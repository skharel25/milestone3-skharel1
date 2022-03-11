from json import load
import os
import random
import string
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
import moviegetter
import GenreFilter
import pdb
import wikifinder

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

# Setting up backend Flask, SQL and FlaskLogin Stuff
app = flask.Flask(__name__)
app.secret_key = os.getenv("app.secret_key")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)


db.create_all()


class UserReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    movieid = db.Column(db.Integer)
    user = db.Column(db.String(25))


db.create_all()

# The first page users will see
@app.route("/")
def login():
    return flask.render_template("login.html")


# For redirecting to the sign up page!
@app.route("/signuppage", methods=["POST"])
def signuppage():
    return flask.redirect(flask.url_for("signup"))


# Just returns the sign up page!
@app.route("/signuppage")
def signup():
    return flask.render_template("signup.html")


# Method for registering new users to DB
@app.route("/registernewuser", methods=["POST"])
def registernewuser():
    try:
        data = flask.request.form
        user_id = data["newuserid"]
        new_user = User(username=user_id)
        db.session.add(new_user)
        db.session.commit()
        flask.flash("User Successfully Created. Try logging in!")
        return flask.redirect(flask.url_for("login"))
    except:
        flask.flash("This user already exists, Usernames must be unique. Try again")
        return flask.redirect(flask.url_for("signup"))


# Method of logging in users
# Takes the user to the main page if login is successful otherwise it returns them to the same login page
@app.route("/loginuser", methods=["POST"])
def loginuser():
    data = flask.request.form
    user_id = data["userid"]

    user = User.query.filter_by(username=user_id).first()
    try:
        login_user(user)
        return flask.redirect(flask.url_for("main"))

    except:
        flask.flash("User does not exist")
        return flask.redirect(flask.url_for("login"))


@app.route("/logoff", methods=["POST"])
def logout():
    logout_user()
    flask.flash("You have been logged out!")
    return flask.redirect(flask.url_for("login"))


# Required part of Flask-Login for loading users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Method for posting user reviews to the database
@app.route("/posttoserver", methods=["POST"])
def posttoserver():
    data = flask.request.form
    rating = data["rating"]
    comment = data["comment"]
    movieid = data["movieid"]
    user = data["user"]
    newreview = UserReview(rating=rating, comment=comment, movieid=movieid, user=user)
    db.session.add(newreview)
    db.session.commit()
    flask.flash("Posted Successfully")
    return flask.redirect(flask.url_for("main"))


bp = flask.Blueprint("bp", __name__, template_folder="./static/react",)


# route for serving React page
@bp.route("/")
def index():
    # NB: DO NOT add an "index.html" file in your normal templates folder
    # Flask will stop serving this React page correctly
    return flask.render_template("index.html")


app.register_blueprint(bp)


@app.route("/returncomments", methods=["POST", "GET"])
def returncomments():
    index = random.randint(0, 14)
    info = moviegetter.moviegetter(index)
    comments = UserReview.query.filter_by(movieid=info[4]).all()
    rating = comments["rating"]
    comment = comments["comment"]
    movieid = comments["movieid"]
    user = comments["user"]

    return flask.jsonify(
        {"Rating": rating, "Comment": comment, "Movieid": movieid, "User": user}
    )


# Main page of the app
# Logining in is required to access this page
@app.route("/main")
def main():
    index = random.randint(0, 14)
    info = moviegetter.moviegetter(index)

    MovieName = info[0]

    Tagline = info[1]

    Genres = str(info[2])

    filteredgenres = GenreFilter.main(Genres)
    # Converting genres to a single string
    genrestring = ""
    length = len(filteredgenres)
    for i in range(0, length):
        if i == length - 1:
            genrestring = genrestring + " " + filteredgenres[i]
        else:
            genrestring = genrestring + " " + filteredgenres[i] + ","

    imageurl = "https://image.tmdb.org/t/p/original/" + info[3]

    pageid = wikifinder.wikifinder(info[0])

    wikiurl = "https://en.wikipedia.org/?curid=" + str(pageid)

    currentuser = current_user.username

    movieid = info[4]

    comments = UserReview.query.filter_by(movieid=movieid).all()
    length = len(comments)
    return flask.render_template(
        "index.html",
        MovieName=MovieName,
        Tagline=Tagline,
        Genres=filteredgenres,
        len=len(filteredgenres),
        imageurl=imageurl,
        wikiurl=wikiurl,
        genrestring=genrestring,
        currentuser=currentuser,
        movieid=movieid,
        comments=comments,
        length=length,
    )


app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)

