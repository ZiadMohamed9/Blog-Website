from flask import Blueprint, render_template, flash, redirect, url_for
from flask_injector import inject
from flask_login import current_user, login_required
from app.services.user import UserService
from app.services.post import PostService
from app.forms.users.edit_form import EditForm


users = Blueprint("users", __name__)

@users.route("/profile")
@login_required
def profile(ps: PostService):
    posts = ps.get_by_author_id(current_user.id)
    return render_template("users/profile.html", posts=posts)

@users.route("/list")
@inject
def list_all(us: UserService):
    if current_user.role != 'Admin':
        return redirect(url_for("users.profile"))
        
    return render_template("users/list.html", users=us.get_all())
    
@users.route("/<public_id>")
@login_required
@inject
def view(us: UserService, public_id):
    if current_user.role != 'Admin':
        return redirect(url_for("users.profile"))
    
    user = us.get_by_public_id(public_id)

    if not user:
        return redirect(url_for("users.list_all"))

    return render_template("users/view.html", user=user)

@users.route("/<public_id>/edit")
@login_required
@inject
def edit(us: UserService, public_id):
    if current_user.role != 'Admin':
        return redirect(url_for("users.profile"))
    
    user = us.get_by_public_id(public_id)
     
    if not user:
        return redirect(url_for("users.list_all"))
    
    edit_form = EditForm()
    edit_form.role.data = user.role

    return render_template("users/edit.html", form=edit_form, user=user)

@users.route("/<public_id>", methods=["POST"])
@login_required
@inject
def update(us: UserService, public_id):
    user = us.get_by_public_id(public_id)

    if not user:
        return redirect(url_for("users.list_all"))

    edit_form = EditForm()

    if edit_form.validate_on_submit():
        us.update_role(user, edit_form.role.data)

        return redirect(url_for("users.list_all"))

    return render_template("users/view.html", user=user)

@users.route("/<public_id>", methods=["DELETE"])
@login_required
@inject
def remove(us: UserService, public_id):
    if current_user.role != 'Admin':
        return redirect(url_for("users.profile"))
    
    user = us.get_by_public_id(public_id)

    if user:
        us.remove_user(user)

    return render_template("users/list.html", users=us.get_all())