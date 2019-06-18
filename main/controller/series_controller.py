from flask import request
from flask_restplus import Resource

from main.service.series_service import SeriesService
from main.util.dto import SeriesDTO, base_args
from webargs import fields
from webargs.flaskparser import use_args

api = SeriesDTO.api

list_all_args = {
    "id": fields.Str(missing=''),
    "title": fields.Str(missing=''),
    "description": fields.Str(missing=''),
}
list_all_args.update(base_args)

service = SeriesService()
dto = SeriesDTO


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid_ Argument', 404: 'Series not found.', 500: 'Mapping Key Error'})
class SeriesCollection(Resource):
    @api.marshal_list_with(dto.query, code=201)
    @use_args(list_all_args)
    def get(self, args):
        """List all series."""
        return service.get_all(args)

    @api.response(201, 'Series successfully created.')
    @api.expect(dto.create)
    def post(self):
        """Creates a new series."""
        return service.upsert(request.json, update=False)

    @api.response(201, 'Series successfully updated.')
    @api.expect(dto.update)
    def put(self):
        """Updates a series."""
        return service.upsert(request.json, update=True)


@api.route('/<int:id_>')
class SeriesItem(Resource):
    @api.marshal_with(dto.list)
    def get(self, id_):
        """Find a series by the ID."""
        return service.get_one(id_)

    @api.response(200, 'Series successfully deleted.')
    def delete(self, id_):
        """Deletes a series."""
        return service.delete(id_, ['books'])


@api.route('/<int:id_>/books')
class SeriesBookCollection(Resource):
    @api.marshal_with(dto.fk_books)
    def get(self, id_):
        """Find the series books."""
        return service.get_model_fk_object(id_, fk='books')


@api.route('/<int:id_>/authors')
class SeriesAuthorCollection(Resource):
    @api.marshal_with(dto.fk_authors)
    def get(self, id_):
        """Find the series authors."""
        return service.get_model_fk_object(id_, fk='authors')
