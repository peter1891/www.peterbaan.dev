from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
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