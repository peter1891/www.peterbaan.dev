from datetime import datetime
from flask_login import UserMixin
import re
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from . import db

class Attribute(db.Model):
    __tablename__ = "web_attributes"

    id = mapped_column(Integer, primary_key=True)
    config_id = mapped_column(ForeignKey("web_configuration.id"))
    config = relationship("Configuration", back_populates="attributes")
    key = mapped_column(String, nullable=False)
    value = mapped_column(String, nullable=False)
    is_type = mapped_column(String, nullable=False)
    icon = mapped_column(String, nullable=False)
    order = mapped_column(Integer)

class Configuration(db.Model):
    __tablename__ = "web_configuration"
    
    id = mapped_column(Integer, primary_key=True)
    website_title = mapped_column(String, nullable=False)
    firstname = mapped_column(String, nullable=False)
    lastname = mapped_column(String, nullable=False)
    job_title = mapped_column(String, nullable=False)
    intro_text = mapped_column(String, nullable=False)
    portrait = mapped_column(String, nullable=False)
    about_text = mapped_column(String, nullable=False)
    attributes = relationship("Attribute", back_populates="config")
    projects = relationship("Project", back_populates="config")

    def validate_image(field):
        if field.data:
            field.data = re.sub(r"[^a-z0-9_.-]", "_", field.data)

class Project(db.Model):
    __tablename__ = "web_projects"
    
    id = mapped_column(Integer, primary_key=True)
    config_id = mapped_column(ForeignKey("web_configuration.id"))
    config = relationship("Configuration", back_populates="projects")
    title = mapped_column(String, nullable=False)
    description_short = mapped_column(String, nullable=False)
    description_long = mapped_column(String, nullable=False)
    creation_date = mapped_column(DateTime, default=datetime.now)

class User(UserMixin, db.Model):
    __tablename__ = "admin_user"
    
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)