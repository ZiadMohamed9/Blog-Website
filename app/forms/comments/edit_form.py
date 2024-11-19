from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    text = StringField(("Text"), validators=[DataRequired()])
