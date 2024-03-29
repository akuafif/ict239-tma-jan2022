from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
#import os
 
def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db':'ict239',
        'host':'127.0.0.1'
    }

    #UPLOAD_FOLDER = app.config['UPLOAD_FOLDER'] = "{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), "csvfile"))

    app.static_folder = 'assets'
    db = MongoEngine(app)

    #COOKIE_TIME_OUT = 60*60*24*7 #7 days
    COOKIE_TIME_OUT = 60*5 #5 minutes

    app.config['SECRET_KEY'] = 'Ny8nyy8ny8nay8nsw8sh'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    #return app, db, login_manager, UPLOAD_FOLDER
    return app, db, login_manager, COOKIE_TIME_OUT

#app, db, login_manager, UPLOAD_FOLDER = create_app()
app, db, login_manager, COOKIE_TIME_OUT = create_app()

