from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
import uuid
from app.models.models import Comment


class CommentService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db
        
    def get_all(self, post_id):
        return Comment.query.filter_by(post_id=post_id).all()
       
    def get_by_id(self, id):
        return Comment.query.filter_by(id=id).first()
    
    def get_by_public_id(self, public_id):
        return Comment.query.filter_by(public_id=public_id).first()
    
    def create_comment(self, text, author_id, post_id):
        comment = Comment(public_id=str(uuid.uuid4()), text=text, author_id=author_id, post_id=post_id)
        self.db.session.add(comment)
        self.db.session.commit()
    
    def update_comment(self, comment, text):
        comment.text = text
        self.db.session.commit()
    
    def delete_comment(self, comment):
        self.db.session.delete(comment)
        self.db.session.commit()