from flask import Flask
app = Flask(__name__)

#app.jinja_env.globals.update(sanitize_html=sanitize_html)
app.config.from_object('config')
from app import views, admin, models
