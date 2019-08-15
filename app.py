"""Adopt application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, Pet, DEFAULT_IMG_URL
from forms import AddPetForm, EditPetForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "SUPER-SECRET-KEY"

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def list_pets():
    """landing page redirecting to list of all users"""
    pets = Pet.query.all()
    return render_template('/show-pets.html', pets=pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """page for form to add pet, only shows form on GET, auto-validates
    inputs on POST, sets default image if photo_url is not provided
    redirects user to homepage with flashed message on succession submit
    """
    form = AddPetForm()

    if form.validate_on_submit():
        pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data.strip() or None,
            age=form.age.data,
            notes=form.notes.data,
        )

        db.session.add(pet)
        db.session.commit()
        flash(f'{pet.name} has been put up for adoption!', "success")
        return redirect("/")

    else:
        return render_template("add-pet-form.html", form=form)


@app.route("/<pet_id>", methods=["GET", "POST"])
def display_pet_details(pet_id):
    """shows pet details and form to edit pet information
    re-renders page on invalid form submission,
    redirects user to homepage with flashed message on successful submit
    """
    form = EditPetForm()
    pet = Pet.query.get(pet_id)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        if not pet.photo_url:
            pet.photo_url = DEFAULT_IMG_URL

        db.session.commit()
        flash(f'{pet.name} has been updated!', "success")
        return redirect("/")

    return render_template("pet-details.html", pet=pet, form=form)
