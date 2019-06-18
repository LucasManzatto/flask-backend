from main.model.series import Series, SeriesSchema
from main.model.books import Book
from faker import Faker
from test.resources.generics import GenericTests

endpoint = 'series'
model = Series
model_schema = SeriesSchema()
filter_by = Series.title
filter_by_key = 'title'
fake = Faker()

generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema, filter_by=filter_by,
                             filter_by_key=filter_by_key)


def test_get_one_series(test_client, db_session):
    generic_tests.get_one(test_client, db_session)


def test_get_all_series(test_client, db_session):
    generic_tests.get_all(test_client, db_session)


def test_get_series_not_found(test_client):
    generic_tests.get_not_found(test_client)


def test_get_series_books(test_client, db_session):
    generic_tests.get_relationship_data(test_client=test_client, db_session=db_session, relationship='books')


def test_get_series_authors(test_client, db_session):
    generic_tests.get_relationship_data(test_client=test_client, db_session=db_session, relationship='authors')


def test_insert_series(test_client, db_session):
    series = Series(title=fake.name(), description='Test')
    generic_tests.insert(db_session, test_client, data=series)


def test_insert_series_duplicated(test_client, db_session):
    generic_tests.insert(db_session, test_client, existing=True)


def test_series_missing_arguments(test_client, db_session):
    generic_tests.insert(db_session, test_client, missing_arguments=True, json_data={})


def test_insert_series_with_books(test_client, db_session):
    series_json = {
        'title': fake.name(),
        'books_ids': [2]
    }
    db_session.commit()
    generic_tests.insert(db_session, test_client, json_data=series_json)


def get_book_ids(db_session):
    books = db_session.query(Book).limit(3).all()
    books_ids = []
    for book in books:
        books_ids.append(book.id)
    return books_ids


def test_update_series(test_client, db_session):
    series_json = {
        'id': 1,
        'title': fake.name(),
        'books_ids': [1]
    }
    generic_tests.insert(db_session, test_client, json_data=series_json, update=True)


def test_delete_series(test_client, db_session):
    series_id = db_session.query(Series).first().id
    generic_tests.delete(db_session=db_session, test_client=test_client, id=series_id)


def test_delete_series_not_found(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=-1, found=False)
