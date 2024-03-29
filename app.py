from flask_login import login_required, current_user
import os
from flask import render_template, request, redirect, send_from_directory
from app import app, db, login_manager

from models.user import User
from blueprints.auth import auth
from blueprints.package import package
from blueprints.admin import admin
app.register_blueprint(auth)
app.register_blueprint(package)
app.register_blueprint(admin)

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'assets'),'favicon.ico',mimetype='image/vnd.microsof.icon')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/layout_test')
def content_layout():
    return render_template('_test_content_layout.html')
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
