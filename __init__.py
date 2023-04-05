from urllib import parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO


# init SQLAlchemy so we can use it later in our models

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)
    driver = '{ODBC Driver 18 for SQL Server}'
    server = 'example.database.windows.net'
    database = 'toolsappdb'
    username = 'REDACTED'
    password = 'REDACTED'
    app.config['SECRET_KEY'] = 'REDACTED'
    params = parse.quote_plus(
        f"Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['BOOTSTRAP_SERVE_LOCAL'] = False
    app.config['BOOTSTRAP_LOAD_REMOTE'] = True
    app.config['BOOTSTRAP_QUERYSTRING_REVVING'] = False
    app.config['BOOTSTRAP_QUERYSTRING_REFRESHING'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import employees

    @login_manager.user_loader
    def load_user(user_id):
        return employees.query.get(int(user_id))

    from views import views
    from auth import auth
    from reports import reports_bp
    from tables import tables_bp
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(reports_bp, url_prefix='/')
    app.register_blueprint(tables_bp, url_prefix='/')

    return app
