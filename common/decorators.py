import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def require_login(func: Callable) -> Callable:
    # decorator_function can inherent all comments from func with @functools.wraps
    # @functools.wraps can be removed form a decorator
    @functools.wraps(func)
    def decorator_function(*args, **kwargs):
        if not session.get("email"):
            flash("You need to log in to access the page", "danger")
            return redirect(url_for('user_blueprint.login_user'))
        return func(*args, **kwargs)
    return decorator_function


def require_admain(func: Callable) -> Callable:
    @functools.wraps(func)
    def decorator_function(*args, **kwargs):
        if session.get("email") != current_app.config.get("ADMIN"):
            flash("You need to be administrator to access the page", "danger")
            return redirect(url_for('user_blueprint.login_user'))
        return func(*args, **kwargs)
    return decorator_function
