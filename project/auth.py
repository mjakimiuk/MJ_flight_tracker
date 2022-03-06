from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = bool(request.form.get("remember"))

    user = db.session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get("email").lower()
    name = request.form.get("name")
    password = request.form.get("password")
    password_check = request.form.get("password_check")

    user = db.session.query(User).filter_by(email=email).first()
    # if this returns a user,
    # then the email already exists in database

    if not all([email, name, password, password_check]):
        flash("Please fill all fields")
        return redirect(url_for("auth.signup"))

    if password != password_check:
        flash("Password does not match")
        return redirect(url_for("auth.signup"))

    if user:
        # if a user is found, we want to
        # redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))

    # create a new user with the form data.
    #  Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
        api_key="",
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
