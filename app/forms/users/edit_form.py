from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, AnyOf

class EditForm(FlaskForm):
    role = StringField("Role", validators=[DataRequired(), AnyOf(["Reader", "Author", "Admin"])])
