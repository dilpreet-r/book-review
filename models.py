import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Users(db.Model):
    __tablename="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)

class Books(db.Model):
    __tablename="books"
    id=db.Column(db.Integer,primary_key=True)
    isbn_no=db.Column(db.String,nullable=False)
    title=db.Column(db.String,nullable=False)
    author=db.Column(db.String,nullable=False)
    year=db.Column(db.Integer,nullable=False)

class Reviews(db.Model):
    __tablename="reviews"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    book_id=db.Column(db.Integer,db.ForeignKey("books.id"),nullable=False)
    rating=db.Column(db.Integer,nullable=False)
    review=db.Column(db.String,nullable=False)

