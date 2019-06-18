from main.model.author import Author, AuthorSchema, author_series
from test.resources.generics import GenericTests
from main.model.books import Book
from faker import Faker
from sqlalchemy import and_

endpoint = 'authors'
model = Author
model_schema = AuthorSchema()
filter_by = Author.name
filter_by_key = 'name'
fake = Faker()

generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema, filter_by=filter_by,
                             filter_by_key=filter_by_key)


def test_get_one_author(test_client, db_session):
    generic_tests.get_one(test_client, db_session)


def test_get_all_authors(test_client, db_session):
    generic_tests.get_all(test_client, db_session)


def test_get_author_books(test_client, db_session):
    generic_tests.get_relationship_data(test_client=test_client, db_session=db_session, relationship='books')


def test_get_author_series(test_client, db_session):
    generic_tests.get_relationship_data(test_client=test_client, db_session=db_session, relationship='series')


def test_get_author_not_found(test_client):
    generic_tests.get_not_found(test_client)


def test_insert_author(test_client, db_session):
    author = Author(name=fake.name())
    generic_tests.insert(db_session, test_client, data=author)


def test_insert_author_duplicated(test_client, db_session):
    generic_tests.insert(db_session, test_client, existing=True)


def test_author_missing_arguments(test_client, db_session):
    generic_tests.insert(db_session, test_client, missing_arguments=True, json_data={})


def test_insert_author_with_series(test_client, db_session):
    author_json = {
        'name': fake.name(),
        'series_ids': [1]
    }
    generic_tests.insert(db_session, test_client, json_data=author_json)


def test_update_author(test_client, db_session):
    author_json = {
        'id': 1,
        'name': fake.name(),
        'series_ids': [1]
    }
    generic_tests.insert(db_session, test_client, json_data=author_json, update=True)


def test_delete_author(test_client, db_session):
    author_books_ids = db_session.query(Author).with_entities(Author.id).join(Book)
    author_series_ids = db_session.query(Author).with_entities(Author.id).join(author_series)
    author_id = db_session.query(Author).filter(
        and_(Author.id.notin_(author_series_ids), Author.id.notin_(author_books_ids))).first().id

    generic_tests.delete(db_session=db_session, test_client=test_client, id=author_id)


def test_delete_author_with_books(test_client, db_session):
    author_books_ids = db_session.query(Author).with_entities(Author.id).join(Book)
    author_id = db_session.query(Author).filter(Author.id.in_(author_books_ids)).first().id

    generic_tests.delete(db_session=db_session, test_client=test_client, id=author_id, has_fk=True)


def test_delete_author_with_series(test_client, db_session):
    author_series_ids = db_session.query(Author).with_entities(Author.id).join(author_series)
    author_id = db_session.query(Author).filter(Author.id.in_(author_series_ids)).first().id

    generic_tests.delete(db_session=db_session, test_client=test_client, id=author_id, has_fk=True)


def test_delete_author_with_series_and_books(test_client, db_session):
    author_books_ids = db_session.query(Author).with_entities(Author.id).join(Book)
    author_series_ids = db_session.query(Author).with_entities(Author.id).join(author_series)
    author_id = db_session.query(Author).filter(
        and_(Author.id.in_(author_series_ids), Author.id.in_(author_books_ids))).first().id

    generic_tests.delete(db_session=db_session, test_client=test_client, id=author_id, has_fk=True)


def test_delete_author_not_found(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=-1, found=False)
