from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import Form, StringField, DecimalField, TextAreaField, PasswordField, SelectField, MultipleFileField, FileField, HiddenField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Regexp

class ImageForm(Form):
    image_id = HiddenField(
        "Image id"
    )
    image = FileField(
        label="Image",
        validators=[FileAllowed(["jpg", "png", "jpeg"])],
        render_kw={"accept": ".jpg, .jpeg, .png"},
    )

class ContactForm(FlaskForm):
    name = StringField(
        label="Name", 
        validators=[DataRequired()]
    )
    email = StringField(
        label="Email", 
        validators=[Email()]
    )
    subject = StringField(
        label="Subject", 
        validators=[DataRequired()]
    )
    message = TextAreaField(
        label="Message", 
        validators=[DataRequired()]
        )
    send = SubmitField(
        "Send"
    )

class LoginForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[DataRequired()]
        )
    password = PasswordField(
        label="Password",
        validators=[DataRequired()]
        )
    login = SubmitField(
        "Login"
    )

class GeneralForm(FlaskForm):
    website_title = StringField(
        label="Website title", 
        validators=[DataRequired()]
    )
    firstname = StringField(
        label="Firstname", 
        validators=[DataRequired()]
    )
    lastname = StringField(
        label="Lastname", 
        validators=[DataRequired()]
    )
    job_title = StringField(
        label="Job title", 
        validators=[DataRequired()]
    )
    intro_text = TextAreaField(
        label="Intro text", 
        validators=[DataRequired()]
    )
    portrait = FileField(
        label="Portrait",
        validators=[FileAllowed(["jpg", "png", "jpeg"])],
        render_kw={"accept": ".jpg, .jpeg, .png"},
    )
    save_general = SubmitField(
        "Save"
    )

class AttributeForm(FlaskForm):
    attribute_type = SelectField(
        label="Type", 
        choices=[("age", "Age"), ("e-mail", "E-mail"), ("name", "Name"), ("residence", "Residence")]
    )
    attribute_type_label = StringField(
        label="Type label"
    )
    attribute_value = StringField(
        label="Value",
        validators=[DataRequired()]
    )
    attribute_order = DecimalField(
        label="Order",
        default=0,
        places=0,
        render_kw={"step": "1", "min": "0"}
    )
    attribute_hidden = HiddenField(
        "Hidden"
    )
    submit = SubmitField(
        "Add"
    )

class SocialForm(FlaskForm):
    attribute_type = SelectField(
        label="Type", 
        choices=[("facebook", "Facebook"), ("github", "Github"), ("linkedIn", "LinkedIn")]
    )
    attribute_type_label = StringField(
        label="Type label"
    )
    attribute_value = StringField(
        label="Value",
        validators=[DataRequired()]
    )
    attribute_order = DecimalField(
        label="Order",
        default=0,
        places=0,
        render_kw={"step": "1", "min": "0"}
    )
    attribute_hidden = HiddenField(
        "Hidden"
    )
    submit = SubmitField(
        "Add"
    )

class AboutForm(FlaskForm):
    about_text = TextAreaField(
        label="About text", 
        validators=[DataRequired()]
    )
    save_about = SubmitField(
        "Save"
    )

class ProjectForm(FlaskForm):
    project_title = StringField(
        label="Project title",
        validators=[DataRequired()],
    )
    description_short = StringField(
        label="Summary",
        validators=[DataRequired()],
    )
    description_long = TextAreaField(
        label="Description",
        validators=[DataRequired()],
    )
    github_url = StringField(
        label="Github URL",
        validators=[DataRequired()],
    )
    thumbnail = FileField(
        label="Thumbnail image",
        validators=[FileAllowed(["jpg", "png", "jpeg"])],
        render_kw={"accept": ".jpg, .jpeg, .png"},
    )
    preview_images = MultipleFileField(
        label="Preview images",
        validators=[FileAllowed(["jpg", "png", "jpeg"])],
        render_kw={"accept": ".jpg, .jpeg, .png"},
    )
    images = FieldList(
        FormField(ImageForm),
        min_entries=0,
        max_entries=None,
    )
    creation_date = HiddenField(
        "Creation date"
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
    