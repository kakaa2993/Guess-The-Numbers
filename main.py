from flask import Flask, render_template, redirect, request, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import requests
from requests import Response
from typing import List, Tuple, Dict, Any

MOVIES_API_KEY: str = "themoviedb.org api_key"  # <- put yours here
MOVIES_SEARCH_API_ENDPOINT: str = "https://api.themoviedb.org/3/search/movie"
POSTER_API_ENDPOINT: str = "https://api.themoviedb.org/3/search/movie"
MOVIE_DETAILS_API: str = "https://api.themoviedb.org/3/movie/"

app: Flask = Flask(__name__)
app.secret_key = "l5df4sdf8dfs4df4sdf4dfs5df8sdf2sdf"  # you need to change this with yours
Bootstrap(app=app)

# Create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_NOTIFICATION"] = False
db: SQLAlchemy = SQLAlchemy(app=app)
app.app_context().push()


# Create table
class Movie(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: str = db.Column(db.String(250), nullable=False, unique=True)
    year: int = db.Column(db.Integer, nullable=False)
    description: str = db.Column(db.String, nullable=False)
    rating: float = db.Column(db.Float, nullable=True)
    ranking: int = db.Column(db.Integer, nullable=True)
    review: str = db.Column(db.String(250), nullable=True)
    img_url: str = db.Column(db.String(250), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id},{self.title},{self.year},{self.description}," \
               f"{self.rating},{self.ranking},{self.review},{self.img_url}"


db.create_all()


# Create the forms for edit rating
class RateMovieForm(FlaskForm):
    rating = FloatField(label="Your Rating Out of 10 e.g 7.3",
                             validators=[DataRequired(), NumberRange(min=0, max=10, message="Out Of Range")])
    review = StringField(label="Your Review",
                              validators=[DataRequired()])
    submit = SubmitField(label="Done")


# Create the forms for adding movies
class AddingMovieForm(FlaskForm):
    movie_title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


# Search for the movie in the movie API
def search_for_movie(user_target: str) -> Response:
    parameters: Dict = {
        "api_key": MOVIES_API_KEY,
        "include_adult": "false",
        "query": user_target,
    }
    response: Response = requests.get(url=MOVIES_SEARCH_API_ENDPOINT, params=parameters).json()["results"]
    return response


# Create the home page that displays all the movies for the database
@app.route("/")
def home() -> str:
    # Read and return the data from the database
    all_movies = Movie.query.order_by(Movie.rating).all()
    # print(all_movies)
    return render_template("index.html", movies=all_movies)


# edit the movie rating and/or review from the database
@app.route("/edit", methods=["POST", "GET"])
def edit_rating() -> Response | str:
    form: RateMovieForm = RateMovieForm()
    movie_id: str | None = request.args.get('id')
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
        # Write inside the labels 'the old review and reading'
        form.rating.render_kw = {"placeholder": f"{movie_data.rating}"}
        form.review.render_kw = {"placeholder": f"{movie_data.review}"}
        return render_template('edit.html', movie_id=movie_id, movie=movie_data, form=form)


# delete the movie from the database
@app.route("/delete", methods=["GET", "POST"])
def delete() -> Response:
    movie_id: str | None = request.args.get("id")
    movie_data = Movie.query.get(movie_id)
    db.session.delete(movie_data)
    db.session.commit()
    return redirect(url_for("home"))


# Add a movie page
@app.route("/add", methods=["POST", "GET"])
def add_movies() -> str:
    form: AddingMovieForm = AddingMovieForm()
    if form.validate_on_submit():
        user_typed: str = form.movie_title.data
        result = search_for_movie(user_typed)
        return render_template("select.html", results=result)
    return render_template("add.html", form=form)


# add the movie selected to the database
@app.route("/to-the-database", methods=["POST", "GET"])
def search_movie_detail_and_add_to_db() -> Response:
    movie_id: str | None = request.args.get("id")
    response: Response = requests.get(url=f"{MOVIE_DETAILS_API}{movie_id}", params={"api_key": MOVIES_API_KEY}).json()
    new_movie = Movie(
        title=response["title"],
        year=response["release_date"].split('-')[0],
        description=response["overview"],
        img_url=f"https://image.tmdb.org/t/p/w500{response['poster_path']}",
        rating=response["vote_average"],
        review=" ",
    )
    db.session.add(new_movie)
    db.session.commit()
    movie_target = Movie.query.filter_by(title=response["title"]).first()
    return redirect(url_for("edit_rating", id=movie_target.id))


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)    # <-- change here
