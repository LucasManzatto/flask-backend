from main.model.books import BookFactory
import factory
from marshmallow import Schema, fields, post_load

from main import db


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Book", back_populates='genres', secondary='book_genres')

    def __init__(self, id=None, name=None, books=None):
        if books is None:
            books = []
        self.id = id
        self.name = name
        self.books = books

    def __repr__(self):
        return f"Genre-ID:{self.id},Name:{self.name}"


class GenreFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Genre
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'Genre %d' % n)

    @factory.post_generation
    def books(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            assert isinstance(extracted, int)
            for book in range(extracted):
                book = BookFactory()
                self.books.append(book)


class GenreSchema(Schema):
    id = fields.Number(allow_none=True)
    name = fields.String(required=True)

    @post_load
    def make_genre(self, data, **kwargs):
        return Genre(**data)
