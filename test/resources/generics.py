from main.util.utils import success, created, conflict, not_found, bad_request
from sqlalchemy.orm import joinedload


class GenericTests:
    def __init__(self, endpoint, model, model_schema, filter_by, filter_by_key):
        self.endpoint = endpoint
        self.model = model
        self.model_schema = model_schema
        self.filter_by = filter_by
        self.filter_by_key = filter_by_key

    def get_one(self, test_client, db_session):
        object_from_db = db_session.query(self.model).first()
        response = test_client.get(f'/{self.endpoint}/{object_from_db.id}')
        assert success(response)
        assert response.json['id'] == object_from_db.id

    def get_relationship_data(self, test_client, db_session, relationship):
        object_from_db = db_session.query(self.model).options(joinedload(relationship)).first()
        relationship_db_objects = object_from_db.__dict__[relationship]
        response = test_client.get(f'/{self.endpoint}/{object_from_db.id}/{relationship}')
        relationship_objects = response.json
        assert success(response)
        if isinstance(relationship_db_objects, list):
            assert len(relationship_db_objects) == len(relationship_objects)
        elif relationship_db_objects:
            assert relationship_db_objects.id == relationship_objects['id']

    def get_all(self, test_client, db_session):
        table_row_size = db_session.query(self.model).count()
        response = test_client.get(f'/{self.endpoint}/')
        response_size = len(response.json['items'])
        assert success(response)
        assert table_row_size == response_size

    def get_not_found(self, test_client):
        response = test_client.get(f'/{self.endpoint}/-1')
        assert not_found(response)

    def insert(self, db_session, test_client, data=None, json_data=None, existing=False, update=False,
               missing_arguments=False):
        if json_data is None:
            json_data = {}
        if existing:
            data = db_session.query(self.model).first()

        if data:
            object_json = self.model_schema.dump(data)
        else:
            object_json = json_data

        if update:
            response = test_client.put(f'/{self.endpoint}/', json=object_json)
        else:
            response = test_client.post(f'/{self.endpoint}/', json=object_json)

        if existing:
            only_one_row = db_session.query(self.model).filter(
                self.filter_by == object_json[self.filter_by_key]).count() == 1
            assert conflict(response)
            assert only_one_row
        elif missing_arguments:
            assert bad_request(response)
        else:
            created_object = db_session.query(self.model).filter(
                self.filter_by == object_json[self.filter_by_key]).first()
            only_one_created = db_session.query(self.model).filter(
                self.filter_by == object_json[self.filter_by_key]).count() == 1
            assert success(response) if update else created(response)
            assert created_object
            assert only_one_created

    def delete(self, db_session, test_client, id, has_fk=False, found=True):
        response = test_client.delete(f'/{self.endpoint}/{id}')
        db_session.commit()
        db_data = self.model.query.get(id)
        if not found:
            assert not_found(response)
        else:
            if has_fk:
                assert conflict(response)
                assert db_data
            else:
                assert success(response)
                assert not db_data
