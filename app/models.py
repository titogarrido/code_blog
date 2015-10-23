from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin, current_user
from app import app
from flask import url_for
import datetime
from webhelpers.text import urlify

db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    email = db.EmailField(max_length=255,unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role, reverse_delete_rule=db.NULLIFY), default=[])

    def __str__(self):
        return '%s' % (self.email)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)
# Create a user to test with
#@app.before_first_request
#def create_user():
#    user_datastore.create_user(email='titogarrido@gmail.com', password='mestre')

# Mail setting
from flask_mail import Mail
mail = Mail(app)

#class Content(db.EmbeddedDocument):
#    content = db.StringField()

class Comment(db.EmbeddedDocument):
    published_date = db.DateTimeField(default=datetime.datetime.now)
    content = db.StringField(required=True)
    author = db.StringField(max_length=120, required=True)

class Post(db.Document):
    title = db.StringField(max_length=120, required=True)
    slug = db.StringField(max_length=255, required=True)
    author = db.ReferenceField(User, required=True)
    tags = db.ListField(db.StringField(max_length=30))
    content = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    published_date = db.DateTimeField(default=datetime.datetime.now)

class Upload(db.Document):
    image_url = db.StringField(required=True, max_length=255)

    def __str__(self):
        return '<img src="%s" />' % (self.image_url)