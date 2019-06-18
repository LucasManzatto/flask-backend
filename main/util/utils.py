from flask_restplus import abort
from flask_restplus._http import HTTPStatus


def not_found(response):
    return response.status_code == HTTPStatus.NOT_FOUND


def success(response):
    return response.status_code == HTTPStatus.OK


def bad_request(response):
    return response.status_code == HTTPStatus.BAD_REQUEST


def conflict(response):
    return response.status_code == HTTPStatus.CONFLICT


def created(response):
    return response.status_code == HTTPStatus.CREATED


def message(response, msg):
    return response.json['message'] == msg


def response_created(msg):
    response_object = {
        'status': 'created',
        'message': msg
    }
    return response_object, HTTPStatus.CREATED


def response_success(msg):
    response_object = {
        'status': 'success',
        'message': msg
    }
    return response_object, HTTPStatus.OK


def response_conflict(msg):
    response_object = {
        'status': 'confict',
        'message': msg,
    }
    return response_object, HTTPStatus.CONFLICT


def response_bad_request(msg):
    return abort(HTTPStatus.BAD_REQUEST, msg)
