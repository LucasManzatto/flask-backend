from main.model.books import BookFactory
from main.model.series import SeriesFactory
from marshmallow import Schema, fields, post_load
import factory
from main import db

author_series = db.Table('author_series', db.Model.metadata,
                         db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                         db.Column('series_id', db.Integer, db.ForeignKey('series.id'))
                         )


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Book", back_populates='author')
    series = db.relationship("Series", back_populates='authors', secondary=author_series)

    def __init__(self, id=None, name=None, books=None):
        if books is None:
            books = []
        self.id = id
        self.name = name
        self.books = books

    def __repr__(self):
        return f"Author-ID:{self.id},Name:{self.name}"


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Author
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'Author %d' % n)

    @factory.post_generation
    def books(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            assert isinstance(extracted, int)
            BookFactory.create_batch(size=extracted, author=self, **kwargs)

    @factory.post_generation
    def series(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            assert isinstance(extracted, int)
            for series in range(extracted):
                series = SeriesFactory()
                self.series.append(series)


class AuthorSchema(Schema):
    id = fields.Number(allow_none=True)
    name = fields.String(required=True)

    @post_load
    def make_author(self, data, **kwargs):
        return Author(**data)
