from main.model.series import Series, SeriesSchema
from main.model.books import Book
from main.service.base_service import BaseService


class SeriesService(BaseService):
    def __init__(self):
        book_fk = {'key': 'books', 'attr_name': 'books_ids', 'fk_model': Book}
        fks = [book_fk]
        super().__init__(model=Series, model_name='Series', schema=SeriesSchema(), filter_by=Series.title,
                         filter_by_key='title', fks=fks)
