from datetime import datetime

import factory
from factory.fuzzy import FuzzyDate
from marshmallow import post_load, Schema, fields

from main import db

book_genres = db.Table('book_genres', db.Model.metadata,
                       db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
                       )


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(30))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', name='fk_book_author'), nullable=True)
    author = db.relationship("Author", back_populates='books')
    series_id = db.Column(db.Integer, db.ForeignKey('series.id', name='fk_book_series'),
                          nullable=True)
    series = db.relationship("Series", back_populates='books')
    genres = db.relationship("Genre", back_populates='books', secondary=book_genres)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())

    def __init__(self, title, description, author=None, series_id=None, author_id=None, id=None, genres=None,
                 series=None, start_date=None, end_date=None
                 ):
        if genres is None:
            genres = []
        self.title = title
        self.description = description
        self.author_id = author_id
        self.series_id = series_id
        self.id = id
        self.genres = genres
        self.series = series
        self.author = author
        self.start_date = start_date
        self.end_date = end_date


def __repr__(self):
    return f"Book: ID:{self.id} ,Title:{self.title} , Author ID:{self.author_id}"


class BookFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Book
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: u'Book %d' % n)
    description = factory.Sequence(lambda n: u'Description %d' % n)
    author = factory.SubFactory('main.model.author.AuthorFactory')
    start_date = FuzzyDate(datetime.now(), datetime(2020, 1, 1))
    end_date = FuzzyDate(datetime(2020, 1, 2), datetime(2022, 1, 1))


class BookWithSeriesFactory(BookFactory):
    title = factory.Sequence(lambda n: u'Book With Series %d' % n)
    series = factory.SubFactory('main.model.series.SeriesFactory')


class BookSchema(Schema):
    id = fields.Integer(allow_none=True)
    title = fields.String(required=True)
    author_id = fields.Number(allow_none=True)
    description = fields.String(allow_none=True)
    series_id = fields.Number(allow_none=True)
    start_date = fields.Date(allow_none=True)
    end_date = fields.Date(allow_none=True)

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)
