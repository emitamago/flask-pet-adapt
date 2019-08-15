from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, AnyOf, NumberRange


class AddPetForm(FlaskForm):
    """form for adding a pet """

    name = StringField(
        "pet name",
        validators=[InputRequired()]
        )

    species = StringField(
        "species",
        validators=[InputRequired(), AnyOf(values=["dog", "cat", "porcupine"])]
        )

    photo_url = StringField(
        "photo url",
        validators=[Optional(), URL()]
        )

    age = IntegerField(
        "age",
        validators=[InputRequired(), NumberRange(min=0, max=30)]
        )

    notes = StringField(
        "notes",
        validators=[Optional()]
        )


class EditPetForm(FlaskForm):
    """form for edit a pet """ 
    photo_url = StringField(
        "photo url",
        validators=[Optional(), URL()]
        )

    notes = StringField(
        "notes",
        validators=[Optional()]
        )

    available = BooleanField(
       "available",
    )
