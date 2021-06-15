from flask import Blueprint, request, render_template, redirect, url_for, session, flash

from models import User, Store
from common.errors import Error


user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            if User.register_user(email, password):
                session["email"] = email
                return redirect(url_for('.login_user'))
        except Error as e:
            print(e.message)
            flash(e, 'danger')

    return render_template("users/register.html")


@user_blueprint.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            if User.is_login_valid(email, password):
                session["email"] = email
                return redirect(url_for('alert_blueprint.index'))

        except Error as e:
            print(e.message)
            flash(e, 'danger')

    return render_template("users/login.html")


@user_blueprint.route("/logout")
def logout_user():
    session["email"] = None
    flash("You have successfully logged out!", 'success')
    return render_template("users/logout.html")
