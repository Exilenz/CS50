import os
import hashlib
import string
import secrets
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///password_manager.db")


# Generate strong passwords
def generate_strong_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# Routes
# Index route


@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Select passwords
    passwords = db.execute("SELECT * FROM passwords WHERE user_id = ?", session["user_id"])

    return render_template("index.html", passwords=passwords)

# Register route


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check password match
        if password != confirmation:
            flash("Passwords are not matching, please try again", "danger")
            return redirect(url_for("register"))

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # Inserting new user
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       username, hashed_password)
        except Exception as e:
            flash("Username already exists, please select different username", "danger")
            return redirect(url_for("register"))

        flash("Registration was successful", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# login route


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(user) != 1 or hashlib.sha256(password.encode()).hexdigest() != user[0]["password"]:
            flash("Username and/or password is not valid. Please try again. If you don't have an account yet please click Register", "danger")
            return redirect(url_for("login"))

        session["user_id"] = user[0]["id"]
        flash("Login successful", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))


@app.route("/add_account", methods=["GET", "POST"])
def add_account():
    if request.method == "POST":
        website = request.form.get("website")
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for unique website and username
        existing_password = db.execute("SELECT * FROM passwords WHERE website = ? AND username = ?",
                                       website, username)

        if existing_password:
            flash("Account with this username on this website already exists.", "danger")
            return redirect(url_for("add_account"))

        # Insert new record
        db.execute("INSERT INTO passwords (user_id, website, username, password) VALUES (?, ?, ?, ?)",
                   session["user_id"], website, username, password)
        flash("Account has been added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("add_account.html")

# Edit route


@app.route("/edit_account/<int:password_id>", methods=["GET", "POST"])
def edit_password(password_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    if request.method == "POST":
        website = request.form.get("website")
        username = request.form.get("username")
        password = request.form.get("password")

         # Check account - username and password
        existing_password = db.execute("SELECT * FROM passwords WHERE website = ? AND username = ? AND id != ? AND user_id = ?",
                                       website, username, password_id, session["user_id"])

        if existing_password:
            flash("This combination of website/platform and username already exists.", "danger")
            return redirect(url_for("edit_password", password_id=password_id))

        # Update account
        db.execute("UPDATE passwords SET website = ?, username = ?, password = ? WHERE id = ? AND user_id = ?",
                   website, username, password, password_id, session["user_id"])
        flash("Account has been edited sucessfully.", "success")
        return redirect(url_for("index"))

    # Edit account
    password_entry = db.execute("SELECT * FROM passwords WHERE id = ? AND user_id = ?", password_id, session["user_id"])
    if len(password_entry) != 1:
        flash("Account not found.", "danger")
        return redirect(url_for("index"))

    return render_template("edit_account.html", password=password_entry[0])

#generate password route

@app.route("/generate_password")
def generate_password():
    password = generate_strong_password()
    return password

# Delete route


@app.route("/delete_account/<int:password_id>")
def delete_password(password_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Delete record from DB
    db.execute("DELETE FROM passwords WHERE id = ? AND user_id = ?",
               password_id, session["user_id"])

    flash("Account has been sucessfully deleted", "success")
    return redirect(url_for("index"))
