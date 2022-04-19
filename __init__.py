from flask import Flask
from flask_login import LoginManager
 
def create_app():
    app = Flask(__name__)
    """app.config['MONGODB_SETTINGS'] = {
        'db':'ict239q1',
        'host':'127.0.0.1'
    }"""

    app.static_folder = 'assets'

    COOKIE_TIME_OUT = 60*60 #60 minutes

    app.config['SECRET_KEY'] = 'Ny8nyy8ny8nay8nsw8sh'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    return app, login_manager, COOKIE_TIME_OUT

app, login_manager, COOKIE_TIME_OUT = create_app()