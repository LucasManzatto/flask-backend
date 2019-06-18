from main.model.author import Author, AuthorSchema
from main.model.series import Series
from main.service.base_service import BaseService
from marshmallow import INCLUDE


class AuthorService(BaseService):
    def __init__(self):
        series_fk = {'key': 'series', 'attr_name': 'series_ids', 'fk_model': Series}
        fks = [series_fk]
        dependencies = ['books', 'series']
        super().__init__(model=Author, model_name='Author', schema=AuthorSchema(unknown=INCLUDE), filter_by=Author.name,
                         filter_by_key='name', fks=fks, dependencies=dependencies)
