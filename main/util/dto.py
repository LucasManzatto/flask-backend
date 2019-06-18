from flask_restplus import fields
from webargs import fields as webargs_fields

from main import api

base_args = {
    "page": webargs_fields.Str(missing=0),
    "per_page": webargs_fields.Str(missing=10),
    "direction": webargs_fields.Str(missing='ASC'),
    "sort_column": webargs_fields.Str(missing='id'),
    "query_all": webargs_fields.Str(missing=''),
}


class AuthorDTO:
    api = api.namespace('authors', description='Operations related to authors.')

    base = api.model("Author_Base", {
        'name': fields.String(description='The name of the author.'),
    })

    create = api.clone("Author_Create", base, {
        'series_ids': fields.List(fields.Integer(required=False, description="The author's series."))
    })
    update = api.clone('Author_Update', create, {
        'id': fields.Integer(description='The ID of the book.'),
    })

    fk_books = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
    })

    fk_series = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the series.'),
        'title': fields.String(required=True, description='The title of the series.'),
        'description': fields.String(required=True, description='The description of the series.')
    })

    list = api.model('Author_List', {
        'id': fields.Integer(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
        'books': fields.Nested(fk_books),
        'series': fields.Nested(fk_series)
    })
    query = api.model('Author_Query', {
        'items': fields.List(fields.Nested(list)),
        'total': fields.Integer(),
        'page': fields.Integer(),
        'per_page': fields.Integer()
    })


class BookDTO:
    api = api.namespace('books', description='Operations related to books.')

    base = api.model('Book_Base', {
        'title': fields.String(required=True, description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
        'start_date': fields.DateTime(description='The start date of the reading.'),
        'end_date': fields.DateTime(description='The end date of the reading.')
    })

    create = api.clone('Book_Update', base, {
        'genre_ids': fields.List(fields.Integer(required=False)),
        'author_id': fields.Integer(required=True, description="The book's author."),
        'series_id': fields.Integer(required=False, description="The book's series.")
    })

    update = api.clone('Book_Create', create, {
        'id': fields.Integer(description='The ID of the book.'),
    })
    fk_author = api.model('Book_Author', {
        'id': fields.Integer(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
    })

    fk_genre = api.model('Book_Genre', {
        'id': fields.Integer(description='The ID of the genre.'),
        'name': fields.String(description='The name of the genre.'),
    })

    fk_series = api.model('Book_Series', {
        'id': fields.Integer(description='The ID of the series.'),
        'title': fields.String(description='The name of the series.'),
        'description': fields.String(description='The description of the series.'),
    })

    list = api.clone('Book_List', base, {
        'id': fields.Integer(description='The ID of the book.'),
        'author': fields.Nested(fk_author),
        'series': fields.Nested(fk_series, allow_null=True),
        'genres': fields.Nested(fk_genre)
    })
    query = api.model('Book_Query', {
        'items': fields.List(fields.Nested(list)),
        'total': fields.Integer(),
        'page': fields.Integer(),
        'per_page': fields.Integer()
    })


class GenreDTO:
    api = api.namespace('genres', description='Operations related to genres.')

    base = api.model('Genre_Base', {
        'name': fields.String(required=True, description='The name of the genre.'),
    })

    create = api.clone('Genre_Update', base, {
        'books_ids': fields.List(fields.Integer(required=False, description="The genre books.")),
    })

    update = api.clone('Genre_Create', create, {
        'id': fields.Integer(description='The ID of the genre.'),
    })
    fk_books = api.model('Genre_Books', {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
    })

    list = api.clone('Genre_List', base, {
        'id': fields.Integer(description='The ID of the genre.'),
        'books': fields.Nested(fk_books)
    })
    query = api.model('Genre_Query', {
        'items': fields.List(fields.Nested(list)),
        'total': fields.Integer(),
        'page': fields.Integer(),
        'per_page': fields.Integer()
    })


class SeriesDTO:
    api = api.namespace('series', description='Operations related to series.')

    base = api.model('Series_Base', {
        'title': fields.String(required=True, description='The title of the series.'),
        'description': fields.String(required=True, description='The description of the series.'),
    })

    create = api.clone('Series_Create', base, {
        'books_ids': fields.List(fields.Integer(required=False, description="The series's books."))
    })

    update = api.clone('Series_Update', create, {
        'id': fields.Integer(description='The ID of the series.'),
    })

    fk_books = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
    })

    fk_authors = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
    })

    list = api.clone('Series_List', base, {
        'id': fields.Integer(description='The ID of the series.'),
        'books': fields.Nested(fk_books),
        'authors': fields.Nested(fk_authors)
    })
    query = api.model('Series_Query', {
        'items': fields.List(fields.Nested(list)),
        'total': fields.Integer(),
        'page': fields.Integer(),
        'per_page': fields.Integer()
    })
