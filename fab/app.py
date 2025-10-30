"""Initialize the Flask application, database session, and appbuilder object."""

from flask import Flask
from flask_appbuilder import AppBuilder
from flask_appbuilder.utils.legacy import get_sqla_class

app = Flask(__name__)
app.config.from_object("config")

db = get_sqla_class()()
appbuilder = AppBuilder()

with app.app_context():
    db.init_app(app)
    appbuilder.init_app(app, db.session)  # type: ignore

    import views  # noqa