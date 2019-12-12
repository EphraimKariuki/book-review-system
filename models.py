import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    secondname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)



class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    reviews = db.relationship("reviews", backref="books", lazy=True)

    def add_review(self, review_id):
        review = Rewiew(id=review_id, book_id=self.id)
        db.session.add(review)
        db.session.commit()


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    rating  =db.Column(db.Integer, nullable=False)
    apirate = db.Column(db.Integer, nullable=False)
    opinion = db.Column(db.String, nullable=False)





if __name__ == "__main__":
        main()
