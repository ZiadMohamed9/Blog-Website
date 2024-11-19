from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
