from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, FileField, HiddenField, SubmitField, Label
from wtforms.validators import DataRequired, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField(
        description="Name", 
        validators=[DataRequired()]
    )
    email = StringField(
        description="Email", 
        validators=[Email()]
    )
    subject = StringField(
        description="Subject", 
        validators=[DataRequired()]
    )
    message = TextAreaField(
        description="Message", 
        validators=[DataRequired()]
        )
    send = SubmitField(
        "Send"
    )

class LoginForm(FlaskForm):
    username = StringField(
        description="Username",
        validators=[DataRequired()]
        )
    password = PasswordField(
        description="Password",
        validators=[DataRequired()]
        )
    login = SubmitField(
        "Login"
    )

class GeneralForm(FlaskForm):
    website_title = StringField(description="Website title", validators=[DataRequired()])
    firstname = StringField(description="Firstname", validators=[DataRequired()])
    lastname = StringField(description="Lastname", validators=[DataRequired()])
    job_title = StringField(description="Job title", validators=[DataRequired()])
    intro_text = TextAreaField(description="Intro text", validators=[DataRequired()])
    portrait = FileField(description="Portrait")
    save_general = SubmitField("Save")

class AboutForm(FlaskForm):
    about_text = TextAreaField(
        description="About text", 
        validators=[DataRequired()]
    )
    save_about = SubmitField(
        "Save"
    )

class AttributeForm(FlaskForm):
    attribute_type = SelectField(
        description="Type", 
        choices=[("age", "Age"), ("email", "E-mail"), ("name", "Name"), ("residence", "Residence")]
    )
    attribute_value = StringField(
        description="Value",
        validators=[DataRequired()]
    )
    attribute_hidden = HiddenField(
        "Hidden"
    )
    submit = SubmitField(
        "Add"
    )

class SocialForm(FlaskForm):
    attribute_type = SelectField(
        description="Type", 
        choices=[("facebook", "Facebook"), ("github", "Github"), ("linkedin", "LinkedIn")]
    )
    attribute_value = StringField(
        description="Value",
        validators=[DataRequired()]
    )
    attribute_hidden = HiddenField(
        "Hidden"
    )
    submit = SubmitField(
        "Add"
    )

class ChangePassForm(FlaskForm):
    current_password = PasswordField(
        description="Current password",
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        description="New password",
        validators=[DataRequired()]
    )
    new_password_check = PasswordField(
        description="Again new password",
        validators=[DataRequired()]
    )
    change_password = SubmitField(
        "Change"
    )
    