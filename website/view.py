from datetime import datetime
from flask import Blueprint, redirect, render_template, url_for

from .core.form import ContactForm
from .core.mail import MailMsg, send_msg

view = Blueprint("view", __name__)

@view.route("/", methods=["GET", "POST"])
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
        return redirect(url_for("view.index"))

    return render_template("index.html", year=datetime.now().year, form=contact_form)