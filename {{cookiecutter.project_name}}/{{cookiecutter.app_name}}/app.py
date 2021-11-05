from flask import Flask
from {{cookiecutter.app_name}} import api, auth, manage
from {{cookiecutter.app_name}}.extensions import apispec, db, jwt, migrate


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("{{cookiecutter.app_name}}")
    app.config.from_object("{{cookiecutter.app_name}}.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.create_admin)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app)
    apispec.spec.components.security_scheme(
        "TokenAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.security_scheme(
        "ApiKeyAuth", {"type": "apiKey", "in": "header", "name": "X-API-Key"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
