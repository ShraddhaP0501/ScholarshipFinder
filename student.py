from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import mysql.connector
from functools import wraps
import os
from dotenv import load_dotenv

stu_bp = Blueprint(
    "student", __name__, url_prefix="/student"
)  # Correct Blueprint setup
bcrypt = Bcrypt()

load_dotenv()


# Database Connection
def db_connection():
    return mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE_NAME"),
    )


# student Registration
@stu_bp.route("/register_stu", methods=["GET", "POST"])
def register_stu():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("student.register_stu"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, hashed_password),
            )
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("student.login_stu"))
        except mysql.connector.IntegrityError:
            flash("Email already registered. Try a different one.", "error")
            return redirect(url_for("student.register_stu"))
        finally:
            conn.close()

    return render_template("register_stu.html")


# student Login
@stu_bp.route("/login", methods=["GET", "POST"])
def login_stu():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session["student_id"] = user[0]
            session["email"] = email
            flash("Login successful!", "success")
            return redirect(url_for("student.dashboard_stu"))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("student.login_stu"))

    return render_template("login_stu.html")


@stu_bp.route("/student/logout")
def logout():
    session.clear()  # Clears entire session
    flash("Logged out successfully.", "success")
    return redirect(url_for("student.login_stu"))


# Protect routes: login required decorator
def login_required_stu(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "student_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("student.login_stu"))
        return f(*args, **kwargs)

    return decorated_function


@stu_bp.route("/dashboard_stu")
@login_required_stu
def dashboard_stu():
    return render_template("dashboard_stu.html", email=session["email"])


@stu_bp.route("/saved_scholarships")
@stu_bp.route("/save_scholarship", methods=["POST"])
def save_scholarship():
    if "user_id" not in session:
        flash("You must be logged in to save scholarships.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    ScholarshipName = request.form["ScholarshipName"]

    cur = mysql.connection.cursor()

    # Check if already saved
    cur.execute(
        "SELECT * FROM saved_scholarships WHERE user_id = %s AND ScholarshipName = %s",
        (user_id, ScholarshipName),
    )
    existing = cur.fetchone()

    if not existing:
        cur.execute(
            "INSERT INTO saved_scholarships (user_id, ScholarshipName) VALUES (%s, %s)",
            (user_id, ScholarshipName),
        )
        mysql.connection.commit()
        flash("Scholarship saved successfully!", "success")
    else:
        flash("You already saved this scholarship.", "info")

    cur.close()
    return redirect(request.referrer)
