from flask import Blueprint, render_template, redirect, url_for, flash
from flask_injector import inject
from flask_login import current_user, login_required
from app.services.post import PostService
from app.forms.posts.create_form import CreateForm
from app.forms.posts.edit_form import EditForm


posts = Blueprint("posts", __name__)

@posts.route("/")
@inject
def list_all(ps: PostService):
    return render_template("posts/list.html", posts=ps.get_all())

@posts.route("/create")
@login_required
def create():
    if current_user.role == 'Reader':
        flash('You must be an author or admin to create posts!', category='error')
        return redirect(url_for("posts.list_all"))
    
    return render_template("/posts/create.html", form=CreateForm())

@posts.route("/", methods=["POST"])
@login_required
@inject
def store(ps: PostService):
    create_form = CreateForm()

    if create_form.validate_on_submit():
        ps.create(
            title=create_form.title.data,
            content=create_form.content.data,
            author_id=current_user.id
        )

        return redirect(url_for("posts.list_all"))

    return render_template("/posts/create.html", form=create_form)

@posts.route("/<public_id>")
@login_required
@inject
def view(ps: PostService, public_id):
    post = ps.get_by_public_id(public_id)

    if not post:
        return redirect(url_for("posts.list_all"))

    return render_template("posts/view.html", post=post)

@posts.route("/<public_id>/edit")
@login_required
@inject
def edit(ps: PostService, public_id):
    if current_user.role == 'Reader':
        flash('You must be an author or admin to edit posts!', category='error')
        return redirect(url_for("posts.list_all"))
    
    post = ps.get_by_public_id(public_id)
     
    if not post:
        return redirect(url_for("posts.list_all"))
    
    if current_user.role == 'Author' and current_user.id != post.author_id:
        flash('You can only edit your own posts!', category='error')
        return redirect(url_for("posts.list_all"))
    
    edit_form = EditForm()
    edit_form.title.data = post.title
    edit_form.content.data = post.content

    return render_template("posts/edit.html", form=edit_form, post=post)

@posts.route("/<public_id>", methods=["POST"])
@login_required
@inject
def update(ps: PostService, public_id):
    post = ps.get_by_public_id(public_id)

    if not post:
        return redirect(url_for("posts.list_all"))

    edit_form = EditForm()

    if edit_form.validate_on_submit():
        ps.update(
            post,
            edit_form.title.data,
            edit_form.content.data
        )

        return redirect(url_for("posts.list_all"))

    return render_template("posts/view.html", post=post)

@posts.route("/<public_id>", methods=["DELETE"])
@login_required
@inject
def delete(ps: PostService, public_id):
    if current_user.role == 'Reader':
        flash('You must be an author or admin to delete posts!', category='error')
        return redirect(url_for("posts.list_all"))
    
    post = ps.get_by_public_id(public_id)

    if current_user.role == 'Author' and current_user.id != post.author_id:
        flash('You can only delete your own posts!', category='error')
        return redirect(url_for("posts.list_all"))
    
    if post:
        ps.delete(post)
        flash('Post is deleted successfully!', category='success')

    return render_template("posts/list.html", posts=ps.get_all())