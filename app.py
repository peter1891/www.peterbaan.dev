from website import create_app
from flask import render_template, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
import os
from form import ContactForm
from mail import send_msg

load_dotenv()

app = create_app()
app.secret_key = os.getenv("APP_SECRET")

@app.route("/", methods=["GET", "POST"])
def index():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        msg = f"Naam: {contact_form.name.data}\nEmail: {contact_form.email.data}\nOnderwerp: {contact_form.subject.data}\nBericht: {contact_form.message.data}"
        send_msg(msg)
        return redirect(url_for(index))

    current_year = datetime.now().year
    return render_template("index.html", year=current_year, form=contact_form)
    
@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)