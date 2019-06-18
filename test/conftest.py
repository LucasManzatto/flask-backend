import pytest
from main import create_app, db
from main.model.series import SeriesFactory
from main.model.author import Author, AuthorFactory

from main.model.books import Book, BookFactory, BookWithSeriesFactory
from main.model.genre import Genre, GenreFactory
from manage import blueprint


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app('test')
    flask_app.register_blueprint(blueprint)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module', autouse=True)
def init_database(test_client):
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())

    BookFactory.reset_sequence()
    AuthorFactory.reset_sequence()
    SeriesFactory.reset_sequence()
    GenreFactory.reset_sequence()

    BookFactory()
    BookWithSeriesFactory()
    AuthorFactory()
    AuthorFactory(books=1)
    AuthorFactory(series=1)
    AuthorFactory(books=1, series=1)
    SeriesFactory()
    GenreFactory()
    GenreFactory(books=1)

    db.session.commit()
    yield db


@pytest.fixture(scope='session')
def _db():
    return db
