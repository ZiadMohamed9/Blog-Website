from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
import uuid
from app.models.models import Like


class LikeService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db
        
    def add_like(self, author_id, post_id):
        like = Like(public_id=str(uuid.uuid4()), author_id=author_id, post_id=post_id)
        self.db.session.add(like)
        self.db.session.commit()
        
    def get_likes_by_post_id_and_author_id(self, post_id, author_id):
        return Like.query.filter_by(author_id=author_id, post_id=post_id).first()
    
    def delete_like(self, like):
        self.db.session.delete(like)
        self.db.session.commit()
        