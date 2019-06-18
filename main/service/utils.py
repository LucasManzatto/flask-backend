from main import db
from sqlalchemy import or_, and_
import re


def get_query(model, args):
    """Create 2 queries, one to query all columns and one to filter by column. Also check if it needs to query a foreign
    key.

    :param model: The model to create the query.
    :param args: The arguments of the query passed by the user.
    :return: A tuple of the query all and the column queries
    """
    query_all = args.pop('query_all', '')
    queries_all_columns = []
    queries_by_column = []

    for key in args:
        foreign_key = re.split("_", key)
        if len(foreign_key) == 2:
            child_model = get_class_by_tablename(foreign_key[0])
            child_key = foreign_key[1]
            queries_all_columns.append(create_query(child_model, child_key, query_all))
            queries_by_column.append(create_query(child_model, child_key, args[key]))
        else:
            queries_all_columns.append(create_query(model, key, query_all))
            queries_by_column.append(create_query(model, key, args[key]))

    queries_all_columns = or_(*tuple(queries_all_columns))
    queries_by_column = and_(*tuple(queries_by_column))
    return queries_all_columns, queries_by_column


def create_query(model, key, query):
    return getattr(model, key).like(f'%{query}%')


def get_sort_query(args, model):
    """ Create the sort query, setting the direction(ASC or DESC) and the column to sort. It also checks if the column
    is a foreign key

    :param args: The direction and sort_column
    :param model: The model do create the query
    :return: The query based on the arguments
    """
    direction = args.pop('direction', 'ASC')
    sort_column = args.pop('sort_column', 'id')
    sort_by_fk = re.split('_', sort_column)
    if len(sort_by_fk) == 2:
        model = get_class_by_tablename(sort_by_fk[0])
        sort_column = sort_by_fk[1]
    return getattr(model, sort_column).desc() if direction.upper() == 'DESC' else getattr(model, sort_column).asc()


def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c
