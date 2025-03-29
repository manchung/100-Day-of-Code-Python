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

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    name = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

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


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    results = db.session.execute(db.select(BlogPost).order_by(BlogPost.date.desc()))
    posts = [post for post in results.scalars()]
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show-post/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    result = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))
    requested_post = result.scalar_one_or_none()
    # requested_post = "Grab the post from your database"
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new-post', methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            body=form.body.data,
            author=form.name.data,
            img_url=form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    form = CreatePostForm()
    post_to_edit = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar_one_or_none()
    if form.validate_on_submit():
        post_to_edit.title = form.title.data
        post_to_edit.subtitle = form.subtitle.data
        post_to_edit.body = form.body.data
        post_to_edit.author = form.name.data
        post_to_edit.img_url = form.img_url.data
        db.session.commit()
        # return redirect(url_for("get_all_posts"))
        return redirect(url_for("show_post", post_id=post_to_edit.id))
    else:
        form.title.data = post_to_edit.title
        form.subtitle.data = post_to_edit.subtitle
        form.body.data = post_to_edit.body
        form.name.data = post_to_edit.author
        form.img_url.data = post_to_edit.img_url
        return render_template("make-post.html", form=form, post=post_to_edit)

# TODO: delete_post() to remove a blog post from the database
@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    post_to_delete = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar_one_or_none()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
