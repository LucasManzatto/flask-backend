from flask import request
from flask_restplus import Resource

from main.service.author_service import AuthorService
from main.util.dto import AuthorDTO, base_args
from webargs import fields
from webargs.flaskparser import use_args

api = AuthorDTO.api

list_all_args = {
    "id": fields.Str(missing=''),
    "name": fields.Str(missing='')
}
list_all_args.update(base_args)

service = AuthorService()
dto = AuthorDTO


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created.', 400: 'Invalid_ Argument', 404: 'Author not found.', 500: 'Mapping Key Error'})
class AuthorCollection(Resource):
    @api.marshal_list_with(dto.query, code=201)
    @use_args(list_all_args)
    def get(self, args):
        """List all authors."""
        return service.get_all(args)

    @api.expect(dto.create)
    def post(self):
        """Creates a new author."""
        return service.upsert(request.json, update=False)

    @api.expect(dto.update)
    def put(self):
        """Updates an author."""
        return service.upsert(request.json, update=True)


@api.route('/<int:id_>')
class BookItem(Resource):
    @api.marshal_with(dto.list)
    def get(self, id_):
        """Find a author by the ID."""
        return service.get_one(id_)

    @staticmethod
    def delete(id_):
        """Deletes an author."""
        return service.delete(id_)


@api.route('/<int:id_>/books')
class BookCollection(Resource):
    @api.marshal_list_with(dto.fk_books)
    def get(self, id_):
        """Find the author books."""
        return service.get_model_fk_object(id_, 'books')


@api.route('/<int:id_>/series')
class BookCollection(Resource):
    @api.marshal_list_with(dto.fk_series)
    def get(self, id_):
        """Find the author series."""
        return service.get_model_fk_object(id_, 'series')
