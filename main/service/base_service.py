from main import db
from main.service import utils
from main.util.utils import response_success, response_conflict, response_created, response_bad_request
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload


class BaseService:

    def __init__(self, model, model_name, schema, filter_by, filter_by_key, fks, dependencies=None, joins=None):
        if joins is None:
            joins = []
        if dependencies is None:
            dependencies = []
        self.model = model
        self.schema = schema
        self.filter_by = filter_by
        self.filter_by_key = filter_by_key
        self.fks = fks
        self.model_name = model_name
        self.dependencies = dependencies
        self.joins = joins

    def upsert(self, data, update):
        """
        Create or update a row. First it check if the json is valid, then check if the object already exists in the
        database, if it doesn't exist call the update or create function based on the update parameter
        :param data: Data in JSON to be created or updated
        :param update: Boolean value to tell if it's a create or update
        :return: Success if created or updated, bad request if JSON is wrong, or conflict if object already exists
        """
        fk_objects = self.get_fk(data, self.fks)
        try:
            new_item = self.schema.load(data)
        except ValidationError as err:
            return response_bad_request(err.messages)

        item = self.model.query.filter(self.filter_by == data[self.filter_by_key]).first()
        if item:
            return response_conflict(f'{self.model_name} already exists. Please choose another value.')
        else:
            return self.update_item(data) if update else self.create(new_item, fk_objects)

    def get_fk(self, data, fks):
        """
        Cria um array de objetos do tipo {key,value} a partir dos IDs recebidos do usuário.
        :param data: Objeto com os IDs recebidos
        :param fks: Objeto com {fk_model,attr_name} para filtrar o objeto data
        :return: Retorna um array de {key,value}
        """
        fk_objects = []
        for fk in fks:
            model = fk['fk_model']
            ids = self.get_ids(data, fk)
            if ids:
                items = model.query.filter(model.id.in_(ids)).all()
                fk_objects.append({'key': fk['key'], 'value': items})
        return fk_objects

    @staticmethod
    def get_ids(data, fk):
        """Como o método in_ só aceita
        arrays, é necessário transfomar o ID em array quando é um relacionamento one-to-many ou one-to-one
        :param data: Objeto com os IDs recebidos
        :param fk: Propriedade onde os IDs estão armazenados
        :return: Uma lista com os IDs
        """
        ids = data.pop(fk['attr_name'], [])
        return ids if isinstance(ids, list) else [ids]

    def create(self, data, fk_objects):
        """ Adiciona o objeto recebido ao banco. Antes de adicionar é necessário algumas verificações e mudanças na
        data.O ID deve ser deletado e deve ser setado as FK ao objeto. Como existem 2 casos, many-to-one e many-to-many
        ,é necessário tratar os dois casos, porque as FKs são recebidas como array e no caso de many-to-one é
        necessário transformar em um dict.
        :param data: Objeto que será inserido no banco em formato dict
        :param fk_objects: Array {key,value} onde a chave é onde será inserido na data, e value é o valor que será
        inserido
        :return: Resposta 201 CREATED.
        """
        del data.id
        self.set_fks_to_object(data, fk_objects)

        db.session.add(data)
        db.session.commit()
        return response_created(f'{self.model_name} successfully created.')

    @staticmethod
    def set_fks_to_object(data, fk_objects):
        for fk in fk_objects:
            try:
                setattr(data, fk['key'], fk['value'])
            except AttributeError as err:
                if len(fk['value']) == 1:
                    setattr(data, fk['key'], fk['value'][0])

    def update_item(self, data):
        self.model.query.filter_by(id=data['id']).update(data)
        db.session.commit()
        return response_success(f'{self.model_name} successfully updated.')

    def get_all(self, args):
        """
        Retornar todos os elementos de uma tabela, com paginação e sort
        :param args: Parâmetros da query passados pelo usuário
        :return:
        """
        page = int(args.pop('page', 0))
        page_size = int(args.pop('per_page', 10))
        sort_query = utils.get_sort_query(args, self.model)
        sub_queries = utils.get_query(self.model, args)
        base_query = self.create_base_query()
        query_filter = base_query.filter(*sub_queries).order_by(sort_query).paginate(page=page, error_out=False,
                                                                                     max_per_page=page_size)
        return query_filter

    def create_base_query(self):
        """
        Cria uma base query do tipo Model.query.join('FK_Model1').join('FK_Model2')
        .options(joinedload('table_name1'),joinedload('table_name2')) para quando a tabela precisa do join para a query
        Se não houver join a query será apenas Model.query
        :return:
        """
        base_query = self.model.query
        options = None
        for join in self.joins:
            base_query = base_query.join(join['join_model'])
            options = joinedload(join['joinedload']) if not options else options.joinedload(join['joinedload'])
        if options:
            base_query = base_query.options(options)
        return base_query

    def get_one(self, id_):
        return self.model.query.get_or_404(id_)

    def get_model_fk_object(self, id, fk):
        item = self.model.query.get(id)
        return getattr(item, fk)

    def delete(self, id_, fks_array=None):
        """
        Deletes an object from the database. Deletion occurs when the object is found and has no dependencies.If it can
        be delete, it first empties all fk references.
        :param id_: ID of the object to be deleted
        :param fks_array: array with all the foreign keys to empty the table
        :return: Success, conflict or bad request.
        """
        if fks_array is None:
            fks_array = []
        item = self.model.query.get(id_)
        if item:
            if self.has_no_dependencies(item, self.dependencies):
                for fk in fks_array:
                    setattr(item, fk, [])
                self.model.query.filter_by(id=id_).delete()
                db.session.commit()
                return response_success('')
            else:
                return response_conflict(
                    f'{self.model_name} has dependencies {self.dependencies} and cannot be deleted.')
        else:
            return response_bad_request(f'{self.model_name} not found.')

    @staticmethod
    def has_no_dependencies(item, dependencies):
        """
        Based on an array of dependencies, check if the item has no dependencies.
        :param item: Item to be checked
        :param dependencies: Array with the dependencies as strings
        :return: True if has no dependencies, False if has.
        """
        for dependency in dependencies:
            if getattr(item, dependency):
                return False
        return True
