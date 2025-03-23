from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ReadOnly, Disabled
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

load_dotenv()

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

bootstrap = Bootstrap5(app)

class Book(db.Model):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()

# all_books = []

class AddBookForm(FlaskForm):
    title = StringField(label='Book Name', validators=[DataRequired()])
    author = StringField(label='Book Author', validators=[DataRequired()])
    rating = DecimalField(label='Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField(label='Add Book')

class EditBookForm(FlaskForm):
    title = StringField(label='Book Name', render_kw={'disabled':''})
    author = StringField(label='Book Author', render_kw={'disabled':''})
    rating = DecimalField(label='Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField(label='Edit Book')

@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = []
        # print(all_books)
        for book in result.scalars():
            # print(book)
            # print(f'id: {book.id}  title: {book.title}  author: {book.author}  rating: {book.rating}')
            all_books.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'rating': book.rating,
                'edit_url': url_for('edit', id=book.id),
                'delete_url': url_for('delete', id=book.id)
            })
        return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    add_form = AddBookForm()
    # if request.method == 'POST':
    #     title = request.form['title']
    #     author = request.form['author']
    #     rating = request.form['rating']
    #     # print(f'title:{title} author:{author} rating:{rating}')
    #     all_books.append({
    #         'title': title,
    #         'author': author,
    #         'rating': rating
    #     })
    #     # print(all_books)
    #     return home()
    # else:
    #     return render_template('add.html')
    if add_form.validate_on_submit():
        title = add_form.title.data
        author = add_form.author.data
        rating = add_form.rating.data
        # all_books.append({
        #     'title': title,
        #     'author': author,
        #     'rating': rating
        # })
        with app.app_context():
            new_book = Book(title=title, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html', form=add_form)

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    edit_form = EditBookForm()
    if edit_form.validate_on_submit():
        new_rating = edit_form.rating.data
        print(f'new_rating: {new_rating}')
        with app.app_context():
            book = db.get_or_404(Book, id)
            book.rating = new_rating
            db.session.commit()
        return redirect(url_for('home'))
    else:
        book = db.get_or_404(Book, id)
        edit_form.title.data = book.title
        edit_form.author.data = book.author
        edit_form.rating.data = book.rating
        return render_template('edit.html', form=edit_form)

@app.route("/delete/<id>")
def delete(id):
    with app.app_context():
        book = db.get_or_404(Book, id)
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

