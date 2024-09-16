import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", False)
    CREATE_DATABASE_IF_NOT_FOUND = os.getenv("CREATE_DATABASE_IF_NOT_FOUND", True)
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    SECRET_KEY = os.getenv("SECRET_KEY")
    LOGIN_MANAGER_LOGIN_VIEW = os.getenv("LOGIN_MANAGER_LOGIN_VIEW", "auth.login")