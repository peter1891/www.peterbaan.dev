from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from . import db, ICON_DICT
from .core.form import AttributeForm, SocialForm, ProjectForm
from .core.models import Attribute, Configuration, Project

OBJECT_MAP = {
    "attribute": (Attribute, "admin.about", "admin/new-attribute.html", "Attribute"),
    "project": (Project, "admin.projects", "admin/new-project.html", "Project"),
    "social": (Attribute, "admin.about", "admin/new-attribute.html", "Social Media"),
}

store = Blueprint("store", __name__)

@store.route("/add/<obj_type>", methods=["GET", "POST"])
@login_required
def add_object(obj_type):
    obj_model, obj_url, obj_html, obj_name = OBJECT_MAP[obj_type]

    configuration = db.session.execute(db.select(Configuration).where(Configuration.id == "1")).scalar()
    print(obj_type)

    if obj_type == "attribute":
        form = AttributeForm(
            attribute_hidden = "attribute"
        )
    elif obj_type == "social":
        form = SocialForm(
            attribute_hidden = "social"
        )
    elif obj_type == "project":
        current_date = datetime.now().strftime("%d-%m-%Y")
        form = ProjectForm(
            creation_date = current_date
        )

    if form.validate_on_submit():
        print("Saving object")

        if obj_type == "project":
            object_to_add = Project(
                config_id = configuration.id,
                title = form.project_title.data,
                description_short = form.description_short.data,
                description_long = form.description_long.data,
                github_url = form.github_url.data,
            )
        else:
            icon = ICON_DICT[form.attribute_type.data]

            object_to_add = Attribute(
                config_id = configuration.id,
                key = form.attribute_type.data,
                value = form.attribute_value.data,
                is_type = form.attribute_hidden.data,
                icon = icon,
                order = 0,
            )

        db.session.add(object_to_add)
        db.session.commit()
        print("Object saved")

        return redirect(url_for(obj_url))

    return render_template(
        obj_html,
        configuration=configuration, 
        title="Add " + obj_name,
        form=form,
        year=datetime.now().year, 
        logged_in=current_user.is_authenticated
    )

@store.route("/edit/<obj_type>/<int:obj_id>", methods=["GET", "POST"])
@login_required
def edit_object(obj_type, obj_id):
    obj_model, obj_url, obj_html, obj_name = OBJECT_MAP[obj_type]

    configuration = db.session.execute(db.select(Configuration).where(Configuration.id == "1")).scalar()

    object_to_edit = db.session.execute(db.select(obj_model).where(obj_model.id == obj_id)).scalar()

    if obj_type == "attribute":
        form = AttributeForm(
            attribute_type = object_to_edit.key,
            attribute_value = object_to_edit.value,
        )
    elif obj_type == "social":
        form = SocialForm(
            attribute_type = object_to_edit.key,
            attribute_value = object_to_edit.value,
        )
    elif obj_type == "project":
        form = ProjectForm(
            project_title = object_to_edit.title,
            description_short = object_to_edit.description_short,
            description_long = object_to_edit.description_long,
            github_url = object_to_edit.github_url,
        )

    form.submit.label.text = "Save"

    if form.validate_on_submit():
        if obj_type == "project":
            object_to_edit.title = form.project_title.data
            object_to_edit.description_short = form.description_short.data
            object_to_edit.description_long = form.description_long.data
            object_to_edit.github_url = form.github_url.data
        else:
            object_to_edit.key = form.attribute_type.data
            object_to_edit.value = form.attribute_value.data

        db.session.commit()

        return redirect(url_for(obj_url))

    return render_template(
        obj_html,
        configuration=configuration, 
        title="Edit " + obj_name,
        form=form,
        object=object_to_edit,
        logged_in=current_user.is_authenticated
    )

@store.route("/delete/<obj_type>/<int:obj_id>")
@login_required
def delete_object(obj_type, obj_id):
    obj_model, obj_url, obj_html, obj_name = OBJECT_MAP[obj_type]

    object_to_delete = db.session.execute(db.select(obj_model).where(obj_model.id == obj_id)).scalar()
    db.session.delete(object_to_delete)
    db.session.commit()
    return redirect(url_for(obj_url))