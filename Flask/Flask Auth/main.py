from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar_one_or_none()



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Check if the email already exists
        existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
        if existing_user:
            flash("Email already exists. Please log in.")
            return redirect(url_for('login'))
        
        # Create a new user
        new_user = User(email=email, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('secrets', name=name))
    else:
        return render_template("register.html")
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('secrets', name=user.name))
            else:
                flash("Invalid credentials. Please try again.")
                return redirect(url_for('login'))
        else:
            flash("Email not found. Please register.")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route('/secrets/<name>')
@login_required
def secrets(name):
    return render_template("secrets.html", name=name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    return send_from_directory('static/files', 'cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)



# pbkdf2:sha256:1000000$BXtA7aGY$fb2fc8553ec78dfab10b9d4f563af4b0c5a77003f6b4306c9738487814253f74
# pbkdf2:sha256:1000000$GVbXy6pN$692355347309afd35fc59284e8199f5d333e9709c49deffe2c2cd9ad7dd98c3c