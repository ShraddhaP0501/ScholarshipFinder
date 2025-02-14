from flask import Flask, request, render_template, redirect, url_for, flash, session, Blueprint
from flask_bcrypt import Bcrypt
import mysql.connector
from functools import wraps
import os
from dotenv import load_dotenv

bp = Blueprint('institute.py',__name__)
bp.secret_key = "your_secret_key"  # Change this to a secure key
bcrypt = Bcrypt(bp)

# Connect to MySQL Database
def db_connection():
    return mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
    )

# Institute Registration Route
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO institutes (name, email, password_hash) VALUES (%s, %s, %s)", 
                           (name, email, hashed_password))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
            flash("Email already registered. Try a different one.", "error")
            return redirect(url_for("register"))
        finally:
            conn.close()

    return render_template("register.html")

# Institute Login Route
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM institutes WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session['institute_id'] = user[0]  # Store institute ID in session
            session['email'] = email
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))  # Redirect to dashboard
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

# Institute Logout Route
@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

# Protect routes: login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'institute_id' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Dashboard (Only Accessible After Login)
@bp.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome to the dashboard, Institute {session['email']}!"

@bp.route("/add_scholarship", methods=["GET", "POST"])
@login_required
def add_scholarship():
    if request.method == "POST":
        scholarship_name = request.form.get("scholarship_name")
        category = request.form.get("category")
        gender = request.form.get("gender")
        income = request.form.get("income")
        details = request.form.get("details")
        domicile = request.form.get("domicile")
        academic_performance = request.form.get("academic_performance")
        family_income = request.form.get("family_income")
        course = request.form.get("course")
        d2d = request.form.get("d2d")
        class_group = request.form.get("class_group")
        link = request.form.get("link")

        if not scholarship_name or not category or not gender or not income:
            flash("Please fill in all required fields!", "error")
            return redirect(url_for("add_scholarship"))

        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO scholarships 
                (ScholarshipName, Category, Gender, Income, Details, Domicile, AcademicPerformance, FamilyIncome, Course, D2D, ClassGroup, Link) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (scholarship_name, category, gender, income, details, domicile, academic_performance, family_income, course, d2d, class_group, link)
            )
            conn.commit()
            flash("Scholarship added successfully!", "success")
            return redirect(url_for("dashboard"))
        finally:
            conn.close()

    return render_template("add_scholarship.html")


