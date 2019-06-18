
from flask import Blueprint
from main import api

from src.main.controller.genre_controller import api as genres_ns
from src.main.controller.book_controller import api as book_ns
from src.main.controller.author_controller import api as author_ns
from src.main.controller.series_controller import api as series_ns

blueprint = Blueprint('api', __name__)

api.add_namespace(book_ns, path='/books')
api.add_namespace(author_ns, path='/authors')
api.add_namespace(series_ns, path='/series')
api.add_namespace(genres_ns, path='/genres')
