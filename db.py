from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

class Database(SQLAlchemy):

    def __init__(self, app: Flask):
        super().__init__(model_class=Base)
        
        self.init_app(app)

from app import db

class Attribute(db.Model):
    id = mapped_column(Integer, primary_key=True)
    key = mapped_column(String, nullable=False)
    value = mapped_column(String, nullable=False)

class Project(db.Model):
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)
    description_short = mapped_column(String, nullable=False)
    description_long = mapped_column(String, nullable=False)