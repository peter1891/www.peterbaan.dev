from dotenv import load_dotenv
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import os
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, ICON_DICT
from .obj_store import store
from .core.form import GeneralForm, AboutForm, AttributeForm, SocialForm, ChangePassForm
from .core.models import Attribute, Configuration, Image, Project, User

admin = Blueprint("admin", __name__)

admin.register_blueprint(store)

@admin.route("/general", methods=["GET", "POST"])
@login_required
def general():
    configuration = db.session.execute(db.select(Configuration).where(Configuration.id == "1")).scalar()

    general_form = GeneralForm(
        website_title = configuration.website_title,
        firstname = configuration.firstname,
        lastname = configuration.lastname,
        job_title = configuration.job_title,
        intro_text = configuration.intro_text,
        portrait = configuration.portrait.location
    )
    if general_form.save_general.data and general_form.validate_on_submit():
        print("Saving general")
        if general_form.portrait.data:
            image = general_form.portrait.data
            image_name = secure_filename(image.filename)
            image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_name)
            image.save(os.path.join(current_app.root_path, image_path))

            if configuration.portrait:
                configuration.portrait.location = "/" + image_path
            else:
                configuration.portrait = Image(
                    location = "/" + image_path,
                    caption = "Portrait  image"
                )

        
        configuration.website_title = general_form.website_title.data
        configuration.firstname = general_form.firstname.data
        configuration.lastname = general_form.lastname.data
        configuration.job_title = general_form.job_title.data
        configuration.intro_text = general_form.intro_text.data
        db.session.commit()
        print("General saved")
        
        return redirect(url_for("admin.general"))
    
    return render_template(
        "admin/general.html",
        configuration=configuration,
        general_form = general_form,
        year=datetime.now().year, 
        logged_in=current_user.is_authenticated
    )

@admin.route("/about", methods=["GET", "POST"])
@login_required
def about():
    configuration = db.session.execute(db.select(Configuration).where(Configuration.id == "1")).scalar()

    about_form = AboutForm(
        about_text = configuration.about_text
    )
    
    if about_form.save_about.data and about_form.validate_on_submit():
        print("Saving about")
        configuration.about_text = about_form.about_text.data
        db.session.commit()
        print("About saved")
        
        return redirect(url_for("admin.about"))

    return render_template(
        "admin/about.html",
        configuration=configuration,
        about_form = about_form,
        year=datetime.now().year, 
        logged_in=current_user.is_authenticated
    )

@admin.route("/projects")
@login_required
def projects():
    configuration = db.session.execute(db.select(Configuration).where(Configuration.id == "1")).scalar()

    projects_list = db.session.execute(db.select(Project)
                                       .order_by(desc(Project.creation_date))).scalars().all()

    return render_template(
        "admin/projects.html",
        configuration=configuration,
        projects=projects_list, 
        year=datetime.now().year, 
        logged_in=current_user.is_authenticated
    )

@admin.route("/password", methods=["GET", "POST"])
@login_required
def password():
    configuration = db.session.execute(db.select(Configuration).where(Configuration.id == "1")).scalar()

    change_password_form = ChangePassForm()
    
    if change_password_form.change_password.data and change_password_form.validate_on_submit():
        print("Saving password")
        if check_password_hash(current_user.password, change_password_form.current_password.data) and change_password_form.new_password.data == change_password_form.new_password_check.data:
            user = db.session.execute(db.select(User).where(User.id == current_user.id)).scalar()
            user.password = generate_password_hash(
                change_password_form.new_password.data, 
                method="pbkdf2", 
                salt_length=8
            )
            db.session.commit()
            print("Password saved")

    return render_template(
        "admin/password.html",
        configuration=configuration,
        password=change_password_form,
        year=datetime.now().year, 
        logged_in=current_user.is_authenticated
    )