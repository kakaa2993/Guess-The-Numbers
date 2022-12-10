#!/usr/bin/python3
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = "l5df4sdf8dfs4df4sdf4dfs5df8sdf2sdf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_NOTIFICATION"] = False
Bootstrap(app=app)
db = SQLAlchemy(app=app)
app.app_context().push()


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


# create the home page that display all the movies for the database
@app.route("/")
def home():
    # read and return the data from the database
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
