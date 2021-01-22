from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import Register, Login

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "Jody"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def display():
    """Show homepage"""
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form and handle form subs"""
    form = Register()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first.data
        last_name = form.last.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect("/secret")
    else:
        return render_template("register.html", form = form)

@app.route('/login', methods = ["GET", "POST"])
def login():
    """produce login form or handle logging in"""

    form = Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/secret")
        else:
            form.username.errors = ["Incorrect Username/Password Combination"]
    return render_template("login.html", form= form)

@app.route("/secret")
def display_secret():
    """Shows hidden page for logged-in users only"""

    if "username" not in session:
        flash("You need to login to view the secret!")
        return redirect("/")

    else: 
        return render_template("secret.html")

@app.route("logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username")

    return redirect("/")