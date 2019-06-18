from main.model.author import Author
from main.model.books import Book, BookSchema
from main.model.genre import Genre
from main.service.base_service import BaseService
from main.model.series import Series


class BookService(BaseService):
    genres_fk = {'key': 'genres', 'attr_name': 'genre_ids', 'fk_model': Genre}
    author_fk = {'key': 'author', 'attr_name': 'author_id', 'fk_model': Author}
    series_fk = {'key': 'series', 'attr_name': 'series_id', 'fk_model': Series}
    fks = [genres_fk, author_fk, series_fk]

    joins = [{'join_model': Author, 'joinedload': 'author'}]

    def __init__(self):
        super().__init__(model=Book, model_name='Book', schema=BookSchema(), filter_by=Book.title,
                         filter_by_key='title', fks=self.fks, joins=self.joins)
