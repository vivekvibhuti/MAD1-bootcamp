from flask import session

from models import User


def is_loggedin():
    return "user_id" in session


def current_user():
    user_id = session.get("user_id")
    if user_id:
        return User.query.get(user_id)


def is_admin():
    return session.get("role") == "admin"


def is_store_manager():
    return session.get("role") == "store_manager"


def is_allowed_edit():
    return session.get("role") == "store_manager"


def login_required():
    return is_loggedin()
