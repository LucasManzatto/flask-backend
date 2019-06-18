from test.resources.generics import GenericTests
from main.model.genre import Genre, GenreSchema
from faker import Faker

endpoint = 'genres'
model = Genre
model_schema = GenreSchema()
filter_by_key = 'name'
fake = Faker()

generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema, filter_by=model.name,
                             filter_by_key=filter_by_key)


def test_get_one_genre(test_client, db_session):
    generic_tests.get_one(test_client=test_client, db_session=db_session)


def test_get_all_genres(test_client, db_session):
    generic_tests.get_all(test_client=test_client, db_session=db_session)


def test_get_genre_not_found(test_client):
    generic_tests.get_not_found(test_client)


def test_get_genre_books(test_client, db_session):
    generic_tests.get_relationship_data(test_client=test_client, db_session=db_session, relationship='books')


def test_insert_genre(test_client, db_session):
    genre = Genre(name=fake.name())
    generic_tests.insert(db_session=db_session, test_client=test_client, data=genre)


def test_insert_genre_with_id(test_client, db_session):
    genre = Genre(id=1, name=fake.name())
    generic_tests.insert(db_session=db_session, test_client=test_client, data=genre)


def test_insert_genre_with_books(test_client, db_session):
    genre_json = {
        'name': fake.name(),
        'books_ids': [1]
    }
    generic_tests.insert(db_session=db_session, test_client=test_client, json_data=genre_json)


def test_insert_genre_duplicated(test_client, db_session):
    generic_tests.insert(db_session=db_session, test_client=test_client, existing=True)


def test_insert_genre_missing_arguments(test_client, db_session):
    generic_tests.insert(db_session=db_session, test_client=test_client, json_data={}, missing_arguments=True)


def test_update_genre(db_session, test_client):
    genre = Genre(id=1, name=fake.name())
    generic_tests.insert(db_session=db_session, test_client=test_client, update=True, data=genre)


def test_delete_genre(db_session, test_client):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=1)


def test_delete_genre_not_found(db_session, test_client):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=-1, found=False)
