from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
import uuid
from app.models.models import Post


class PostService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self):
        return Post.query.all()
    
    def get_by_id(self, id):
        return Post.query.filter_by(id=id).first()
    
    def get_by_public_id(self, public_id):
        return Post.query.filter_by(public_id=public_id).first()
    
    def get_by_author_id(self, author_id):
        return Post.query.filter_by(author_id=author_id).all()
    
    def get_by_title(self, title):
        return Post.query.filter_by(title=title)

    def create(self, title, content, author_id):
        post = Post(public_id=str(uuid.uuid4()), title=title, content=content, author_id=author_id)
        self.db.session.add(post)
        self.db.session.commit()

    def update(self, post, title, content):
        post.title = title
        post.content = content
        self.db.session.commit()
        
    def delete(self, post):
        self.db.session.delete(post)
        self.db.session.commit()

