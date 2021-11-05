import click
from flask.cli import with_appcontext


@click.command("create-admin")
@with_appcontext
def create_admin():
    """Create a new admin user"""
    from {{cookiecutter.app_name}}.extensions import db
    from {{cookiecutter.app_name}}.models import User

    click.echo("creating user 'admin'")
    user = User(
        username="{{cookiecutter.admin_user_username}}",
        email="{{cookiecutter.admin_user_email}}",
        password="{{cookiecutter.admin_user_password}}",
        active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user 'admin'")
