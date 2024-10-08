from dotenv import load_dotenv
import os

load_dotenv()

from website import create_app

app = create_app()
app.config["SECRET_KEY"] = os.getenv("APP_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("APP_DATABASE")

from db import Database

db = Database(app)

with app.app_context():
    db.create_all()

from datetime import datetime
from flask import render_template, redirect, url_for
from form import ContactForm
from mail import send_msg, MailMsg

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
    
@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)