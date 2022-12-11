#!/usr/bin/python3
from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import requests

MOVIES_API_KEY = "a0d35a0a8d84bd65eb09706947c74399"
MOVIES_SEARCH_API_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
POSTER_API_ENDPOINT = "https://api.themoviedb.org/3/search/movie"

app = Flask(__name__)
app.secret_key = "l5df4sdf8dfs4df4sdf4dfs5df8sdf2sdf"
Bootstrap(app=app)

# Create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_NOTIFICATION"] = False
db = SQLAlchemy(app=app)
app.app_context().push()


# Create table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float(), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False, unique=True)

    def __repr__(self):
        return f"{self.id},{self.title},{self.year},{self.description}," \
               f"{self.rating},{self.ranking},{self.review},{self.img_url}"
db.create_all()


# create the forms for edit rating
class RateMovieForm(FlaskForm):
    rating = FloatField(label="Your Rating Out of 10 e.g 7.3",
                        validators=[DataRequired(), NumberRange(min=0, max=10, message="Out Of Range")])
    review = StringField(label="Your Review",
                         validators=[DataRequired()])
    submit = SubmitField(label="Done")


# Create the forms for add movies
class AddingMovieForm(FlaskForm):
    movie_title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


# Search for the movie in the themoviedb api
def search_for_movie(user_target):
    parameters = {
        "api_key": MOVIES_API_KEY,
        "include_adult": "false",
        "query": user_target,
    }
    response = requests.get(url=MOVIES_SEARCH_API_ENDPOINT, params=parameters).json()["results"]
    # print(response)
    return response



# create the home page that display all the movies for the database
@app.route("/")
def home():
    # read and return the data from the database
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["POST", "GET"])
def edit_rating():
    form = RateMovieForm()
    movie_id = request.args.get('id')
    movie_data = Movie.query.get(movie_id)
    if form.validate_on_submit():
        # change the movie rating and review from the database
        new_rating = form.rating.data
        new_review = form.review.data
        movie_data.rating = new_rating
        movie_data.review = new_review
        db.session.commit()
        return redirect(url_for("home"))
    else:
        # write inside the labels 'the old review and reading'
        form.rating.render_kw = {"placeholder": f"{movie_data.rating}"}
        form.review.render_kw = {"placeholder": f"{movie_data.review}"}
        # return render_template('edit.html', form=form)
        return render_template('edit.html', movie_id=movie_id, movie=movie_data, form=form)


# delete the movie from the database
@app.route("/delete", methods=["GET", "POST"])
def delete():
    movie_id = request.args.get("id")
    movie_data = Movie.query.get(movie_id)
    db.session.delete(movie_data)
    db.session.commit()
    return redirect(url_for("home"))


# Add a movie page
@app.route("/add", methods=["POST", "GET"])
def add_movies():
    form = AddingMovieForm()
    data_needed = []
    if form.validate_on_submit():
        print(form.movie_title.data)
        user_typed = form.movie_title.data
        result = search_for_movie(user_typed)
        for movie in result:
            data = [movie["id"], movie["title"], movie["release_date"]]
            data_needed.append(data)
        print(data_needed)
    return render_template("add.html", form=form, results=data_needed)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
