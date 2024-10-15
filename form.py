from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField(description="Name", 
                       validators=[DataRequired()])
    email = StringField(description="Email", 
                        validators=[Email()])
    subject = StringField(description="Subject", 
                          validators=[DataRequired()])
    message = TextAreaField(description="Message", 
                            validators=[DataRequired()])
    send = SubmitField("Send")

class LoginForm(FlaskForm):
    username = StringField(description="Username",
                           validators=[DataRequired()])
    password = PasswordField(description="Password",
                             validators=[DataRequired()])
    login = SubmitField("Login")

class ChangePassForm(FlaskForm):
    current_password = PasswordField(description="Current password",
                             validators=[DataRequired()])
    new_password = PasswordField(description="New password",
                             validators=[DataRequired()])
    new_password_check = PasswordField(description="new password again",
                             validators=[DataRequired()])
    change = SubmitField("Change")
    