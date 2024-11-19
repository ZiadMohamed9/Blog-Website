from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email, AnyOf

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=4, max=40)])
    username = StringField("Username", validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20), Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", message="should contains at least one lowercase letter, one uppercase letter, and one digit")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = StringField('Role', validators=[DataRequired(), AnyOf(["Reader", "Author", "Admin"])])