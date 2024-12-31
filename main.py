from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user

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


# Create the Database Tables
class Products(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    vendor: Mapped[str] = mapped_column(String(100), nullable=False)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    with app.app_context():
        db.create_all()
