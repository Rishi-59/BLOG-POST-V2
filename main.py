from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# WTFORM
class PostForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Name', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit Post')


with app.app_context():
    db.create_all()


# DATABASE FUNCTIONS
def _get_posts():
    return db.session.scalars(db.select(BlogPost)).all()


def _get_post(post_id):
    return db.session.get(BlogPost, post_id)


def _add_post(post):
    db.session.add(post)
    db.session.commit()


def _delete_post(post_id):
    post = _get_post(post_id)
    db.session.delete(post)
    db.session.commit()


@app.route('/')
def get_all_posts():
    posts = _get_posts()
    posts = [post for post in posts]
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = _get_post(post_id)
    print(requested_post.img_url)
    return render_template("post.html", post=requested_post)


@app.route('/post/new', methods=['GET', 'POST'])
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            body=form.content.data,
            author=form.author.data,
            img_url=form.img_url.data,
        )
        _add_post(post)

        return redirect(url_for('get_all_posts'))

    return render_template("make-post.html", form=form)


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    requested_post = _get_post(post_id)
    form = PostForm(obj=requested_post)
    form.content.data = requested_post.body
    if form.validate_on_submit():
        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        requested_post.date = date.today().strftime("%B %d, %Y")
        requested_post.body = form.content.data
        requested_post.author = form.author.data
        requested_post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))

    return render_template("make-post.html", post=requested_post, form=form)


@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    _delete_post(post_id)
    return redirect(url_for('get_all_posts'))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
