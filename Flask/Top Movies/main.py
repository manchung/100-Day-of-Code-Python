from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(1000), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class EditMovieForm(FlaskForm):
    rating = DecimalField(label='Your Rating Out of 10 e.g. 7.5', validators=[DataRequired(), NumberRange(min=1,max=10)])
    review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField(label='Done')

class AddMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')

with app.app_context():
    db.create_all()

def seed_movies():
    with app.app_context():
        movie_1 = Movie(
            title="Phone Booth",
            year=2002,
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
            rating=7.3,
            ranking=10,
            review="My favourite character was the caller.",
            img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
        )

        movie_2 = Movie(
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=7.3,
            ranking=9,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
        )

        db.session.add(movie_1)
        db.session.add(movie_2)
        db.session.commit()

# seed_movies()

@app.route("/")
def home():
    all_movies = []
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
        all_movies = [movie.as_dict() for movie in result.scalars()]
    return render_template("index.html", movies=all_movies)

@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id):
    edit_form = EditMovieForm()
    if edit_form.validate_on_submit():
        new_rating = edit_form.rating.data
        new_review = edit_form.review.data
        with app.app_context():
            movie = db.get_or_404(Movie, id)
            movie.rating = new_rating
            movie.review = new_review
            db.session.commit()
        return redirect(url_for('home'))
    else:
        with app.app_context():
            movie = db.get_or_404(Movie, id)
            return render_template("edit.html", form=edit_form, movie=movie.as_dict())

@app.route('/delete/<id>')
def delete(id):
    with app.app_context():
        movie = db.get_or_404(Movie, id)
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        title = add_form.title.data
        print(title)
        return redirect(url_for('home'))
    else:

        return render_template('add.html', form=add_form)

if __name__ == '__main__':
    app.run(debug=True)
