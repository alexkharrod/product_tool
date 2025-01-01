from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from forms import  CreateUser, CreateProduct, LoginUser
from functools import wraps
from datetime import date

import os
from load_dotenv import load_dotenv


#basic sql alchemy
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

#setup app
load_dotenv()
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

#initialize bootstrap
Bootstrap5(app)

# initialize the app with the extension
db.init_app(app)

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)


# Create the Database Tables
class Products(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    vendor: Mapped[str] = mapped_column(String(100), nullable=False)


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    fname: Mapped[str] = mapped_column(String(50), nullable=False)
    lname: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    def __init__(self, email: str, fname: str, lname: str, password: str, role: str) -> None:
        self.email = email
        self.fname = fname
        self.lname = lname
        self.password = password
        self.role = role


# login manager user loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = CreateUser()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        existing_user = Users.query.filter_by(email=form.email.data).first()
        if form.email.data == existing_user:
            flash("Email already registered, login here")
            return redirect(url_for("login"))
        else:
            new_user = Users(
                fname=form.fname.data.title(),
                lname=form.lname.data.title(),
                email=form.email.data,
                password=hashed_password,
                role=form.role.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f"{new_user.fname} successfully logged in")
            return redirect(url_for('home'))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash(f"{user.fname} successfully logged in")
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Password didn't match")
                return redirect(url_for("home"))
        else:
            flash("email not registered.  Try again or ask admin to register you")
            return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
def logout():
    flash(f"Logging {current_user.fname} out.")
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    with app.app_context():
        db.create_all()
