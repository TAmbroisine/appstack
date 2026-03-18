import os

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"]}})
    
    # Database configuration from environment variables
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'tododb')
    
    # Use SQLite for local testing if DB_HOST is not set
    if os.getenv('DB_HOST'):
        database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    else:
        database_url = f'sqlite:///{os.path.join(app.instance_path, "flaskr.sqlite")}'
    
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=database_url,
            SQLALCHEMY_DATABASE_URI=database_url,
    )

    if test_config is None:
        # load the instancce config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import tasks
    app.register_blueprint(tasks.bp)
    app.add_url_rule('/', endpoint='index')

    return(app)
