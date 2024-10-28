from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from . import db
from .core.form import LoginForm
from .core.models import Configuration, User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    configuration = db.session.execute(db.select(Configuration).where(Configuration.id == "1")).scalar()

    if current_user.is_authenticated:
        return redirect(url_for("admin.general"))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        user = db.session.execute(
            db.select(User)
            .where(User.username == username)
        ).scalar()

        if not user:
            flash("Unknown user")
        elif not check_password_hash(user.password, login_form.password.data):
            flash("Wrong password")
        else:
            login_user(user)
            return redirect(url_for("admin.general"))

    return render_template(
        "login.html", 
        configuration=configuration,
        year=datetime.now().year, 
        form=login_form, 
        logged_in=current_user.is_authenticated
    )

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))