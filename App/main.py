import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
import json, pathlib
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


from App.database import init_db
from App.config import load_config


from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views, setup_admin

SESSION_FILE = pathlib.Path.home() / ".breadvan_session"

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_admin(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    app.app_context().push()
    return app

def save_session(user_id: str):
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": user_id}, f)

def load_session() -> str | None:
    if SESSION_FILE.exists():
        with open(SESSION_FILE) as f:
            return json.load(f).get("user_id")
    return None

def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()