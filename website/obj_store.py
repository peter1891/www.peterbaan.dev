from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, current_app, request, jsonify
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

from . import db, ICON_DICT
from .core.form import AttributeForm, ImageForm, SocialForm, ProjectForm
from .core.models import Attribute, Configuration, Image, Project

OBJECT_MAP = {
    "attribute": (Attribute, "admin.about", "admin/new-attribute.html", "Attribute"),
    "project": (Project, "admin.projects", "admin/new-project.html", "Project"),
    "social": (Attribute, "admin.about", "admin/new-attribute.html", "Social Media"),
}

def process_image(image_data):
    image = image_data
    image_name = secure_filename(image.filename)
    image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_name)
    image.save(os.path.join(current_app.root_path, image_path))

    return "/" + image_path

def add_image(images: list):
    for image in images:
        image_to_add = Image(
            project_id = image["project_id"],
            location = process_image(image["location"]),
        )
        db.session.add(image_to_add)
        db.session.commit()

def edit_image(images: list):
    for image in images:
        if image["location"].filename:
            image_to_edit = db.session.execute(db.select(Image).where(Image.id == image["id"])).scalar()
            image_to_edit.location = process_image(image["location"])
            db.session.commit()

def delete_image(images: list):
    for image in images:
        image_to_delete = db.session.execute(db.select(Image).where(Image.id == image)).scalar()
        db.session.delete(image_to_delete)
        db.session.commit()

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

        print()

        if obj_type == "project":
            object_to_add = Project(
                config_id = configuration.id,
                title = form.project_title.data,
                description_short = form.description_short.data,
                description_long = form.description_long.data,
                github_url = form.github_url.data,
                thumbnail = "",
                thumbnail_caption = form.project_title.data + " thumbnail image",
            )

            if form.thumbnail.data:
                object_to_add.thumbnail = process_image(form.thumbnail.data)

            preview_images = request.files.getlist('new_preview_images')
            for preview_image in preview_images:
                image = Image(
                    location = process_image(preview_image),
                )
                object_to_add.images.append(image)

        else:
            icon = ICON_DICT[form.attribute_type.data]

            object_to_add = Attribute(
                config_id = configuration.id,
                key = form.attribute_type.data,
                value = form.attribute_value.data,
                is_type = form.attribute_hidden.data,
                icon = icon,
                order = form.attribute_order.data,
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
        title = object_to_edit.key.capitalize()

        form = AttributeForm(
            attribute_type = object_to_edit.key,
            attribute_value = object_to_edit.value,
            attribute_order = object_to_edit.order,
        )
    elif obj_type == "social":
        title = object_to_edit.key.capitalize()
        
        form = SocialForm(
            attribute_type = object_to_edit.key,
            attribute_value = object_to_edit.value,
            attribute_order = object_to_edit.order,
        )
    elif obj_type == "project":
        title = object_to_edit.title

        form = ProjectForm(
            project_title = object_to_edit.title,
            description_short = object_to_edit.description_short,
            description_long = object_to_edit.description_long,
            github_url = object_to_edit.github_url,
            thumbnail = object_to_edit.thumbnail,
        )

        for image in object_to_edit.images:
            image_form = ImageForm(
                image_id = image.id,
                image = image.location,
            )
            form.images.append_entry(image_form)

    form.submit.label.text = "Save"

    if form.validate_on_submit():
        if obj_type == "project":
            object_to_edit.title = form.project_title.data
            object_to_edit.description_short = form.description_short.data
            object_to_edit.description_long = form.description_long.data
            object_to_edit.github_url = form.github_url.data

            if form.thumbnail.data:
                object_to_edit.thumbnail = process_image(form.thumbnail.data)

            image_new = []
            image_current = request.form.getlist('current_preview_images')
            image_delete = [ image.id for image in object_to_edit.images ]

            for img in request.files.getlist('new_preview_images'):
                image_new.append({
                    "project_id": object_to_edit.id, 
                    "location": img,
                    })
                pass

            for img in image_current:
                image_delete.remove(int(img))

            if image_new:
                add_image(image_new)

            if image_delete:
                delete_image(image_delete)

            db.session.commit()
            return jsonify({"redirect": url_for(obj_url)})

        else:
            object_to_edit.key = form.attribute_type.data
            object_to_edit.value = form.attribute_value.data
            object_to_edit.order = form.attribute_order.data

            db.session.commit()
            return redirect(url_for(obj_url))

    return render_template(
        obj_html,
        configuration=configuration, 
        title="Edit " + title,
        form=form,
        object=object_to_edit,
        year=datetime.now().year, 
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