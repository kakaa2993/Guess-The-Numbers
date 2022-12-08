#!/usr/bin/python3
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = ""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_NOTIFICATION"] = False
Bootstrap(app=app)
db = SQLAlchemy(app=app)

class Movies(db.Model):
    pass
@app.route("/")
def home():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

