from app import create_app, db, login_manager
from flask_injector import FlaskInjector, singleton
from app.services.post import PostService
from app.services.user import UserService
from app.services.like import LikeService
from app.services.comment import CommentService


app = create_app()

# Configure and enable Dependency Injection
def configure(binder):
    binder.bind(PostService, to=PostService(db), scope=singleton)
    binder.bind(UserService, to=UserService(db), scope=singleton)
    binder.bind(LikeService, to=LikeService(db), scope=singleton)
    binder.bind(CommentService, to=CommentService(db), scope=singleton)

FlaskInjector(app=app, modules=[configure])

@login_manager.user_loader
def load_user(user_id):
    return UserService(db).get_by_id(user_id)

if __name__ == '__main__':
    if app.config["CREATE_DATABASE_IF_NOT_FOUND"]:
        with app.app_context():
            db.create_all()

    app.run()