from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)

class Attribute(db.Model):
    id = mapped_column(Integer, primary_key=True)
    key = mapped_column(String, nullable=False)
    value = mapped_column(String, nullable=False)

class Project(db.Model):
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)
    description_short = mapped_column(String, nullable=False)
    description_long = mapped_column(String, nullable=False)