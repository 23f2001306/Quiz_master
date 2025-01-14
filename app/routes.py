from flask import render_template
from app import app
from app.forms import LoginForm, SignupForm

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html",form = form)

@app.route("/signup")
def signup():
    form = SignupForm()
    return render_template("signup.html",form = form)