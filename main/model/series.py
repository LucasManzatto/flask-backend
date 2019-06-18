import factory
from marshmallow import post_load, Schema, fields

from main import db


class Series(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(30))
    books = db.relationship("Book", back_populates='series')
    authors = db.relationship("Author", back_populates='series', secondary='author_series')

    def __init__(self, title, description=None, id=None, authors=None, books=None):
        if authors is None:
            authors = []
        if books is None:
            books = []
        self.id = id
        self.title = title
        self.description = description
        self.authors = authors
        self.books = books

    def __repr__(self):
        return f"Series:{self.title}"


class SeriesFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Series
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: u'Series %d' % n)
    description = factory.Sequence(lambda n: u'Description %d' % n)


class SeriesSchema(Schema):
    id = fields.Integer(allow_none=True)
    description = fields.String(allow_none=True)
    title = fields.String(required=True)

    @post_load
    def make_series(self, data, **kwargs):
        return Series(**data)
