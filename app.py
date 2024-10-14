from datetime import datetime
from flask import render_template, redirect, url_for
from flask_login import LoginManager, login_required, logout_user
from form import ContactForm, LoginForm
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

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(
        db.select(User)
        .where(User.id == user_id)
        .scalar()
    )

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

    current_year = datetime.now().year
    return render_template("index.html", year=current_year, form=contact_form)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        pass
    return render_template("login.html", form=login_form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)