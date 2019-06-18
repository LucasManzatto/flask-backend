from flask import request
from flask_restplus import Resource
from main.service.genre_service import GenreService

from main.util.dto import GenreDTO, base_args
from webargs import fields
from webargs.flaskparser import use_args

api = GenreDTO.api

list_all_args = {
    "id": fields.Str(missing=''),
    "name": fields.Str(missing='')
}
list_all_args.update(base_args)

service = GenreService()
dto = GenreDTO


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid_ Argument', 404: 'Genre not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):
    @api.marshal_list_with(dto.query, code=201)
    @use_args(list_all_args)
    def get(self, args):
        """List all genres."""
        return service.get_all(args)

    @api.expect(dto.create)
    def post(self):
        """Creates a new genre."""
        return service.upsert(data=request.json, update=False)

    @api.expect(dto.update)
    def put(self):
        """Updates a genre."""
        return service.upsert(data=request.json, update=True)


@api.route('/<int:id_>')
class BookItem(Resource):
    @staticmethod
    @api.marshal_with(dto.list)
    def get(id_):
        """Find a genre by the ID."""
        return service.get_one(id_)

    @staticmethod
    def delete(id_):
        """Deletes a genre."""
        return service.delete(id_, ['books'])


@api.route('/<int:id_>/books')
class GenreBookCollection(Resource):
    @api.marshal_with(dto.fk_books)
    def get(self, id_):
        """Find the genre books."""
        return service.get_model_fk_object(id_, fk='books')
