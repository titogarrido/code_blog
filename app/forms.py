from flask.ext.mongoengine.wtf import model_form
from models import Comment

CommentForm = model_form(Comment, exclude=['published_date'])