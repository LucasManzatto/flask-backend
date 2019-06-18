from main.model.genre import GenreSchema, Genre
from main.model.books import Book
from main.service.base_service import BaseService


class GenreService(BaseService):
    def __init__(self):
        book_fk = {'key': 'books', 'attr_name': 'books_ids', 'fk_model': Book}
        fks = [book_fk]
        super().__init__(model=Genre, model_name='Genre', schema=GenreSchema(), filter_by=Genre.name,
                         filter_by_key='name', fks=fks)
