from flask import Blueprint, flash, redirect, url_for, jsonify, render_template
from flask_login import login_required, current_user
from app.services.post import PostService
from app.services.like import LikeService
from app.services.comment import CommentService
from app.forms.comments.create_form import CreateForm
from app.forms.comments.edit_form import EditForm
from flask_injector import inject


actions = Blueprint('actions', __name__)

@actions.route('/like-post/<post_id>', methods=['POST'])
@login_required
@inject
def like_post(ps: PostService, ls: LikeService, post_id):
    post = ps.get_by_id(post_id)
    like = ls.get_likes_by_post_id_and_author_id(post_id, current_user.id)

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        ls.delete_like(like)
    else:
        ls.add_like(current_user.id, post_id)

    return redirect(url_for('posts.list_all'))

@actions.route("/comments/<post_id>/create")
@login_required
def add_comment(post_id):
    return render_template("/comments/create.html", form=CreateForm(), post_id=post_id)

@actions.route("/comments/<post_id>")
@inject
def list_comments(cs: CommentService, post_id):
    return render_template("comments/list.html", comments=cs.get_all(post_id), post_id=post_id)

@actions.route('/comments/<post_id>', methods=['POST'])
@inject
@login_required
def save_comment(cs: CommentService, post_id):
    create_form = CreateForm()
        
    if create_form.validate_on_submit():
        cs.create_comment(
            text=create_form.text.data,
            author_id=current_user.id,
            post_id=post_id
        )
        return redirect(url_for('actions.list_comments', post_id=post_id))

    return render_template("comments/create.html", form=create_form)

@actions.route('/comments/<post_id>/<public_id>/edit')
@inject
@login_required
def edit_comment(cs: CommentService, post_id, public_id):
    comment = cs.get_by_public_id(public_id)
    
    if not comment:
        flash('Comment does not exist.', category='error')
    
    if current_user.id != comment.author_id:
        flash('You do not have permission to edit this comment.', category='error')
        
    edit_form = EditForm()
    edit_form.text.data = comment.text
    
    return render_template("comments/edit.html", form=edit_form, post_id=post_id, public_id=public_id)

@actions.route("/comments/<post_id>/<public_id>", methods=["POST"])
@login_required
@inject
def update_comment(cs: CommentService, public_id, post_id):
    comment = cs.get_by_public_id(public_id)
    
    if not comment:
        flash('Comment does not exist.', category='error')

    edit_form = EditForm()

    if edit_form.validate_on_submit():
        cs.update_comment(
            comment,
            edit_form.text.data
        )

    return redirect(url_for("actions.list_comments", post_id=post_id))
        
@actions.route("/comments/<post_id>/<public_id>/delete")
@inject
@login_required
def delete_comment(cs: CommentService, public_id, post_id):
    comment = cs.get_by_public_id(public_id)

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author_id and current_user.id != comment.post.author_id and current_user.role != "Admin":
        flash('You do not have permission to delete this comment.', category='error')
    else:
        cs.delete_comment(comment)

    return redirect(url_for('actions.list_comments', post_id=post_id))