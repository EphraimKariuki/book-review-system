import os
import csv
import requests


from flask import Flask, session, render_template, request,session, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")

#
@app.route("/signup", methods=["GET","POST"])
def signup():

    #Get the user's information.
    first = request.form.get("first")
    second = request.form.get("second")
    email = request.form.get("email")
    password = request.form.get("password")

    #Ensure that every field is filled.
    if first == "" or second == "" or email == "" or password == "":
        return render_template("error.html", message = "Fill all fields.")

    #Ensure that no two users use the same email to sign up.
    user = db.execute("SELECT * FROM users WHERE (email = :email)", {"email": email}).fetchone()
    if user is None:
         db.execute("INSERT INTO users (firstname, secondname, email, password) VALUES(:firstname, :secondname, :email, :password)", {"firstname": first, "secondname": second, "email": email,"password": password})
         db.commit()
         return render_template("success.html", message = "You have successfuly been signed up!", first = first)
    else:
         return render_template("error.html", message = "A user with the same email exists. Kindly Sign up using another email.")






@app.route("/signin", methods=["GET", "POST"])
def signin():
    return render_template('signin.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = db.execute("SELECT * FROM users WHERE (email= :email) and (password= :password)", {"email":email , "password": password}).fetchone()
    if user is None:
        return render_template("signin.html")
    else:
        return redirect("search")





@app.route("/search", methods=["GET","POST"])
def search():

    #Get the user's search query.
    searchQuery = str(request.form.get('searchContent'))
    searchQuery = searchQuery.title()


    books = db.execute("SELECT * FROM books WHERE (title LIKE :title) or (author LIKE :author) or (isbn= :isbn)", {"title": "%"+searchQuery+"%", "author": "%"+searchQuery+"%", "isbn": searchQuery}).fetchall()
    return render_template("search.html", books=books)


@app.route("/books", methods=["GET", "POST"])
def books():

    # Display the selected book's detail
    book_id = int(request.form.get('book'))
    book = db.execute("SELECT * FROM books WHERE (id = :id)", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html")
    return render_template("books.html", book=book)

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/books/<int:book_id>", methods=["GET", "POST"])
def review(book_id):

    # Get review from goodreads API.
    # res =  requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"t052dnowfmqDZ9TdbWqZQ", "isbn": })
    user_id = 7
    rating = int(request.form.get('rating'))
    apirate = 4
    opinion = request.form.get('comment')

    db.execute("INSERT INTO reviews (user_id, book_id, rating, apirate, opinion) VALUES(:user_id, :book_id, :rating, :apirate, :opinion)", {"user_id": user_id, "book_id": book_id, "rating": rating, "apirate": apirate, "opinion": opinion})
    db.commit()

    message = "You have successfully made your review!"
    return redirect(url_for('goodreads'))
    # return render_template("success.html", message=message)


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/goodreads")
def goodreads():

    # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "t052dnowfmqDZ9TdbWqZQ", "isbns": isbn})
    # data = res.json()
    return render_template("goodreads.html" )



if __name__ == "__main__":
    with app.app_context():
        main()
