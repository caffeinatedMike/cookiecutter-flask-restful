from flask import Blueprint, current_app, jsonify
from marshmallow import ValidationError
from {{cookiecutter.app_name}}.extensions import apispec
from {{cookiecutter.app_name}}.api.resources import UserResource, UserList
from {{cookiecutter.app_name}}.api.schemas import UserSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")


blueprint.add_url_rule(
    "/users/<int:user_id>",
    view_func=UserResource.as_view("user_by_id"),
    endpoint="user_by_id"
)
blueprint.add_url_rule("/users", view_func=UserList.as_view("users"), endpoint="users")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
