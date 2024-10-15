from datetime import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from form import ContactForm, LoginForm, ChangePassForm
from mail import send_msg, MailMsg
from dotenv import load_dotenv
import os
from website import create_app
from db import db, Attribute, Project, User

load_dotenv()

app = create_app()
app.config["SECRET_KEY"] = os.getenv("APP_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("APP_DATABASE")

# setup database
db.init_app(app)

with app.app_context():
    db.create_all()

    if not db.session.execute(db.select(User)).scalars().all():
        password = generate_password_hash(
            os.getenv("ADMIN_PASSWORD"),
            method="pbkdf2", 
            salt_length=8
        )

        admin = User(
            username = "admin",
            password = password
        )

        db.session.add(admin)
        db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(
        db.select(User)
        .where(User.id == user_id)
    ).scalar()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def index():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        msg = MailMsg(
            name=contact_form.name.data,
            email=contact_form.email.data,
            subject=contact_form.subject.data,
            message=contact_form.message.data,
        )
        
        send_msg(msg)
        return redirect(url_for("index"))

    return render_template("index.html", year=datetime.now().year, form=contact_form)
    
@app.route("/login", methods=["GET", "POST"])
def login():
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
            return redirect(url_for("admin"))

    return render_template("login.html", year=datetime.now().year, form=login_form, logged_in=current_user.is_authenticated)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/admin")
@login_required
def admin():
    change_password_form = ChangePassForm()
    return render_template("admin.html", year=datetime.now().year, password=change_password_form, logged_in=current_user.is_authenticated)

if __name__ == "__main__":
    app.run(debug=True)