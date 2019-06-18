from main.model.books import Book, BookSchema

from test.resources.generics import GenericTests
from faker import Faker
from sqlalchemy.orm import joinedload

endpoint = 'books'
model = Book
model_schema = BookSchema()
filter_by = Book.title
filter_by_key = 'title'
fake = Faker()

generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema, filter_by=filter_by,
                             filter_by_key=filter_by_key)


def test_get_one_book(test_client, db_session):
    generic_tests.get_one(test_client=test_client, db_session=db_session)


def test_get_all_books(test_client, db_session):
    generic_tests.get_all(test_client=test_client, db_session=db_session)


def test_get_book_not_found(test_client):
    generic_tests.get_not_found(test_client)


def test_get_book_author(db_session, test_client):
    generic_tests.get_relationship_data(db_session=db_session, test_client=test_client, relationship='author')


def test_get_book_series(db_session, test_client):
    generic_tests.get_relationship_data(db_session=db_session, test_client=test_client, relationship='series')


def test_get_book_genres(db_session, test_client):
    generic_tests.get_relationship_data(db_session=db_session, test_client=test_client, relationship='genres')


def test_insert_book(test_client, db_session):
    book = Book(title=fake.name(), description='Teste', author_id=1)
    generic_tests.insert(db_session=db_session, test_client=test_client, data=book)


def test_insert_book_with_id(test_client, db_session):
    book = Book(id=1, title=fake.name(), description='Teste', author_id=1)
    generic_tests.insert(db_session=db_session, test_client=test_client, data=book)


def test_insert_book_with_genres(test_client, db_session):
    book_json = {
        'title': fake.name(),
        'description': 'test',
        'author_id': 1,
        'genre_ids': [1]
    }
    generic_tests.insert(db_session=db_session, test_client=test_client, json_data=book_json)

# TODO: test insert com todas as propriedades e checar se todas as propriedades foram inseridas corretamente no banco


def test_insert_book_duplicated(test_client, db_session):
    generic_tests.insert(db_session=db_session, test_client=test_client, existing=True)


def test_insert_book_missing_arguments(test_client, db_session):
    generic_tests.insert(db_session=db_session, test_client=test_client, json_data={}, missing_arguments=True)


def test_update_book(db_session, test_client):
    book = Book(id=1, title=fake.name(), description='Test', author_id=1)
    generic_tests.insert(db_session=db_session, test_client=test_client, update=True, data=book)


def test_delete_book(db_session, test_client):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=1)


def test_delete_book_not_found(db_session, test_client):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=-1, found=False)
