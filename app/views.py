from flask import render_template, request, redirect, url_for
from app import app
from models import Post, Upload, Comment
from flask.ext.security import login_required

from forms import CommentForm



import jinja2
import scrubber
from app.libs.htmltruncate import truncate

def sanitize_html(text):
    return jinja2.Markup(scrubber.Scrubber().scrub(text))

def truncate_html(text):
    return truncate(text,150)


app.jinja_env.filters['sanitize_html'] = sanitize_html
app.jinja_env.filters['truncate_html'] = truncate_html


@app.route('/')
@app.route('/index')
def index(page=1):
    paginated_posts = Post.objects.order_by("+published_date")
    tags=Post.objects.distinct('tags')
    return render_template("index.html",
        title = 'Home', paginated_posts=paginated_posts, tags=tags)

@app.route('/galeria')
@login_required
def galeria():
    fotos = Upload.objects
    return render_template('galeria.html', fotos=fotos)

@app.route('/post/<slug>',methods=['GET','POST'])
def post(slug):
    p=Post.objects.get_or_404(slug=slug)
    tags=Post.objects.distinct('tags')
    print request.form
    form = CommentForm(request.form)
    print form.data
    print form.validate()
    if form.validate():
        comment = Comment()
        form.populate_obj(comment)
        p.comments.append(comment)
        p.save()
        return redirect(url_for('post', slug=slug))

    return render_template("post.html", title = p.title, p=p, tags=tags, form=form)