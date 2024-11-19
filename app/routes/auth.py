from flask import Blueprint, render_template, redirect, url_for
from flask_injector import inject
from app.services.user import UserService
from flask_login import login_required
from app.forms.auth.login_form import LoginForm
from app.forms.auth.signup_form import SignupForm

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
@inject
def login(us: UserService):
    login_form = LoginForm()

    error_message = ""

    if login_form.validate_on_submit():
        if us.login(login_form.username.data, login_form.password.data):
            return redirect(url_for("users.profile"))

        error_message = "incorrect username or password"

    return render_template("/auth/login.html", form=login_form, error_message=error_message)

@auth.route("/signup", methods=["GET", "POST"])
@inject
def signup(us: UserService):
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        if not us.get_by_username(username=signup_form.username.data):
            us.signup(
                signup_form.name.data,
                signup_form.username.data,
                signup_form.email.data,
                signup_form.password.data,
                signup_form.role.data
            )

        return redirect(url_for("auth.login"))

    return render_template("/auth/signup.html", form=signup_form)

@auth.route("/logout")
@login_required
@inject
def logout(us: UserService):
    us.logout()
    
    return redirect(url_for("dashboard.home"))