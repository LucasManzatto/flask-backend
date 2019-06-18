from flask import request
from flask_restplus import Resource

from main.service.book_service import BookService
from main.util.dto import BookDTO, base_args
from webargs import fields
from webargs.flaskparser import use_args

api = BookDTO.api

list_all_args = {
    "id": fields.Str(missing=''),
    "title": fields.Str(missing=''),
    "description": fields.Str(missing=''),
    'author_name': fields.Str(missing='')
}
list_all_args.update(base_args)

service = BookService()
dto = BookDTO


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid_ Argument', 404: 'Book not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):

    @api.marshal_list_with(dto.query, code=201)
    @use_args(list_all_args)
    def get(self, args):
        """List all books."""
        return service.get_all(args)

    @api.expect(dto.create)
    def post(self):
        """Creates a new book."""
        return service.upsert(request.json, update=False)

    @api.expect(dto.update)
    def put(self):
        """Updates a book."""
        return service.upsert(request.json, update=True)


@api.route('/<int:id_>')
class BookItem(Resource):
    @api.marshal_with(dto.list)
    def get(self, id_):
        """Find a book by the ID."""
        return service.get_one(id_)

    @staticmethod
    def delete(id_):
        """Deletes a book."""
        return service.delete(id_)


@api.route('/<int:id_>/author')
class BookAuthorItem(Resource):
    @api.marshal_with(dto.fk_author)
    def get(self, id_):
        """Find the book's author."""
        return service.get_model_fk_object(id_, 'author')


@api.route('/<int:id_>/genres')
class BookGenreCollection(Resource):
    @api.marshal_with(dto.fk_genre)
    def get(self, id_):
        """Find the book genres."""
        return service.get_model_fk_object(id_, 'genres')


@api.route('/<int:id_>/series')
class BookSeriesItem(Resource):
    @api.marshal_with(dto.fk_series)
    def get(self, id_):
        """Find the book series."""
        return service.get_model_fk_object(id_, 'series')
