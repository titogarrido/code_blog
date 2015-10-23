# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask.ext.admin import Admin, BaseView, expose, form
from flask.ext.admin.base import MenuLink
from app import app
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView
from models import User, Post, Upload
from flask.ext.security import login_required, logout_user, current_user
from flask import redirect, url_for, request, flash, render_template
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from config import UPLOADS_DEFAULT_DEST
from flask.ext.admin.contrib import fileadmin
import os.path as op

# Add administrative views here
admin = Admin(name='Admin')
# Add views here
admin.init_app(app)

uploads = UploadSet('uploads', IMAGES)
configure_uploads(app, uploads)

def get_image_url(id):
    photo = Upload.objects.get_or_404(id=id)
    return uploads.url(photo.image_url)
app.jinja_env.filters['get_image_url'] = get_image_url

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = uploads.save(request.files['photo'])
        rec = Upload(image_url=filename)
        rec.save()
        flash("Photo saved.")
        return redirect(url_for('galeria'))
    return render_template('upload.html')

# all admin views should subclass AuthMixin
class AuthMixin(object):
    def is_accessible(self):
        if current_user.is_authenticated():
            return True
        return False

class MyView(AuthMixin,BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class AuthenticatedFileView(fileadmin.FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated()

@app.route('/logout/')
def logout_view():
    logout_user()
    return redirect(url_for('index'))


class UserView(AuthMixin,ModelView):
    can_create = False
    column_list = ('email','active')
    column_filters = ['email']
    column_searchable_list = ('email',)

class UploadView(AuthMixin,ModelView):
    form_extra_fields = {
        'image_url': form.FileUploadField('Upload',
                                      base_path=UPLOADS_DEFAULT_DEST+uploads.name)
    }

class PostView(AuthMixin,ModelView):
    edit_template = 'admin/model/ckeditor_edit.html'
    create_template = 'admin/model/ckeditor_edit.html'
    column_searchable_list = ('title','content',)
    column_filters = ['published_date']
    form_widget_args = {
        'content': {
            'class': 'ckeditor'
        }
    }
    form_subdocuments = {
        'comments': {
            'form_subdocuments': {
                None: {
                    # Add <hr> at the end of the form
                    'form_rules': ('author', 'content', rules.HTML('<hr>')),
                    'form_widget_args': {
                        'content': {
                            'class': 'ckeditor'
                        }
                    }
                }
            }
        },
        }
    form_ajax_refs = {
        'author': {
            'fields': ('email',),
            'page_size': 10
        }
    }


admin.add_view(UserView(User, name='Usuários'))
admin.add_view(PostView(Post, name='Posts'))
admin.add_view(UploadView(Upload, name='Uploads'))
admin.add_view(AuthenticatedFileView(op.join(op.dirname(__file__), 'static/files'), '/files/', name='Arquivos'))
admin.add_link(MenuLink(name='Voltar', url='/'))
admin.add_link(MenuLink(name='Sair', endpoint='logout_view'))