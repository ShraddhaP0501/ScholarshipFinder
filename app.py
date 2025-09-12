import mysql.connector
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from datetime import datetime
from institute import bp as institute_bp
from student import stu_bp as student_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"
#changes done
# Register the Blueprint
app.register_blueprint(institute_bp)
app.register_blueprint(student_bp)

load_dotenv()


def getdatabase():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
        )
        return conn
    except mysql.connector.Error as e:
        print("Database connection error:", e)
        return None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/find", methods=["GET", "POST"])
def findscholarship():
    scholarships = None  # Ensure it's None on initial page load
    try:
        if request.method == "POST":  # Only search when form is submitted
            category = request.form.get("category")
            gender = request.form.get("gender")
            income = request.form.get("income")

            conn = getdatabase()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT ScholarshipName, Details, Domicile, AcademicPerformance, FamilyIncome, Course,D2D, ClassGroup,Link, checkstatus FROM scholarships 
                   WHERE category = %s AND gender = %s AND income = %s""",
                (category, gender, income),
            )
            scholarships = cursor.fetchall()

            cursor.close()
            conn.close()
    except Exception as e:
        print("Error:", e)

    return render_template("home.html", scholarships=scholarships)


@app.route("/search", methods=["GET"])
def search_scholarship():
    try:
        query = request.args.get("query", "").strip()
        scholarships = []
        scholarship_names = []
        print(query)
        conn = getdatabase()
        if conn:
            cursor = conn.cursor(dictionary=True)

            # Fetch all scholarship names for the datalist
            cursor.execute("SELECT DISTINCT ScholarshipName FROM scholarships")
            scholarship_names = [row["ScholarshipName"] for row in cursor.fetchall()]

            # Fetch search results if a query is provided
            if query:
                sql_query = "SELECT DISTINCT ScholarshipName, Details,Domicile,AcademicPerformance,FamilyIncome,Course,D2D,ClassGroup,Link, checkstatus FROM scholarships WHERE ScholarshipName LIKE %s"
                cursor.execute(sql_query, (f"%{query}%",))
                scholarships = cursor.fetchall()

            cursor.close()
            conn.close()
        else:
            print("❌ Database connection failed.")

        return render_template(
            "search_results.html",
            scholarships=scholarships,
            query=query,
            scholarship_names=scholarship_names,  # Pass names for datalist
        )
    except Exception as e:
        print("⚠️ Error in search functionality:", e)
        return f"An error occurred while searching for scholarships: {e}"


@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "").strip()
    suggestions = []

    if len(query) >= 3:
        conn = getdatabase()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT ScholarshipName FROM scholarships WHERE ScholarshipName LIKE %s LIMIT 10",
                (f"%{query}%",),
            )
            suggestions = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

    return jsonify(suggestions)


@app.route("/allscholarships", methods=["GET"])
def allscholarships():
    try:
        conn = getdatabase()
        if not conn:
            return "Error: Unable to connect to the database."
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT ScholarshipName, Details,Domicile,AcademicPerformance,FamilyIncome,Course,D2D,ClassGroup,Link,checkstatus FROM scholarships"
        )
        all_scholarships = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template(
            "all-scholarship.html", all_scholarships=all_scholarships
        )
    except Exception as e:
        print("Error fetching all scholarships:", e)
        return "Error: Unable to retrieve data."

    # Route to display OBC scholarships


@app.route("/general-scholarships")
def general_scholarships():
    try:
        conn = getdatabase()
        cursor = conn.cursor()

        today = datetime.today().strftime("%Y-%m-%d")

        query_active = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance,FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus FROM scholarships 
            WHERE category = 'general' AND end_date >= %s
        """
        query_inactive = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance, 
                            FamilyIncome, Course, D2D, ClassGroup, Link, checkstatus
            FROM scholarships 
            WHERE category = 'general' AND end_date < %s
        """

        cursor.execute(query_active, (today,))
        active_scholarships = cursor.fetchall()

        cursor.execute(query_inactive, (today,))
        inactive_scholarships = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "general_scholarship.html",
            active_scholarships=active_scholarships,
            inactive_scholarships=inactive_scholarships,
        )
    except Exception as e:
        print(e)
        return "Error fetching General scholarships"


# Route to display SEBC scholarships
@app.route("/sebc-scholarships")
def sebc_scholarships():
    try:
        conn = getdatabase()
        cursor = conn.cursor()

        today = datetime.today().strftime("%Y-%m-%d")

        query_active = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance,FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus FROM scholarships 
            WHERE category = 'general' AND end_date >= %s
        """
        query_inactive = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance, 
                            FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus 
            FROM scholarships 
            WHERE category = 'general' AND end_date < %s
        """

        cursor.execute(query_active, (today,))
        active_scholarships = cursor.fetchall()

        cursor.execute(query_inactive, (today,))
        inactive_scholarships = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "sebc_scholarship.html",
            active_scholarships=active_scholarships,
            inactive_scholarships=inactive_scholarships,
        )
    except Exception as e:
        print(e)
        return "Error fetching SEBC scholarships"


# Route to display OBC scholarships
@app.route("/obc-scholarships")
def obc_scholarships():
    try:
        conn = getdatabase()
        cursor = conn.cursor()
        today = datetime.today().strftime("%Y-%m-%d")

        query_active = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance,FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus FROM scholarships 
            WHERE category = 'general' AND end_date >= %s
        """
        query_inactive = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance, 
                            FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus 
            FROM scholarships 
            WHERE category = 'general' AND end_date < %s
        """

        cursor.execute(query_active, (today,))
        active_scholarships = cursor.fetchall()

        cursor.execute(query_inactive, (today,))
        inactive_scholarships = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "obc_scholarship.html",
            active_scholarships=active_scholarships,
            inactive_scholarships=inactive_scholarships,
        )
    except Exception as e:
        print(e)
        return "Error fetching OBC scholarships"


# Route to display ST scholarships
@app.route("/st-scholarships")
def st_scholarships():
    try:
        conn = getdatabase()
        cursor = conn.cursor()
        today = datetime.today().strftime("%Y-%m-%d")

        query_active = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance,FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus FROM scholarships 
            WHERE category = 'general' AND end_date >= %s
        """
        query_inactive = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance, 
                            FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus
            FROM scholarships 
            WHERE category = 'general' AND end_date < %s
        """

        cursor.execute(query_active, (today,))
        active_scholarships = cursor.fetchall()

        cursor.execute(query_inactive, (today,))
        inactive_scholarships = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "st_scholarship.html",
            active_scholarships=active_scholarships,
            inactive_scholarships=inactive_scholarships,
        )
    except Exception as e:
        print(e)
        return "Error fetching ST scholarships"


# Route to display SC scholarships
@app.route("/sc-scholarships")
def sc_scholarships():
    try:
        conn = getdatabase()
        cursor = conn.cursor()
        today = datetime.today().strftime("%Y-%m-%d")

        query_active = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance,FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus FROM scholarships 
            WHERE category = 'general' AND end_date >= %s
        """
        query_inactive = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance, 
                            FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus
            FROM scholarships 
            WHERE category = 'general' AND end_date < %s
        """

        cursor.execute(query_active, (today,))
        active_scholarships = cursor.fetchall()

        cursor.execute(query_inactive, (today,))
        inactive_scholarships = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "sc_scholarship.html",
            active_scholarships=active_scholarships,
            inactive_scholarships=inactive_scholarships,
        )
    except Exception as e:
        print(e)
        return "Error fetching SC scholarships"


# Route to display EWS scholarships
@app.route("/ews-scholarships")
def ews_scholarships():
    try:
        conn = getdatabase()
        cursor = conn.cursor()
        today = datetime.today().strftime("%Y-%m-%d")

        query_active = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance,FamilyIncome, Course, D2D, ClassGroup, Link,checkstatus FROM scholarships 
            WHERE category = 'general' AND end_date >= %s
        """
        query_inactive = """
            SELECT DISTINCT ScholarshipName, Details, Domicile, AcademicPerformance, 
                            FamilyIncome, Course, D2D, ClassGroup, Link, checkstatus
            FROM scholarships 
            WHERE category = 'general' AND end_date < %s
        """

        cursor.execute(query_active, (today,))
        active_scholarships = cursor.fetchall()

        cursor.execute(query_inactive, (today,))
        inactive_scholarships = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "ews_scholarship.html",
            active_scholarships=active_scholarships,
            inactive_scholarships=inactive_scholarships,
        )
    except Exception as e:
        print(e)
        return "Error fetching EWS scholarships"


@app.route("/SpecialScholarship", methods=["GET"])
def SpecialScholarships():
    try:
        conn = getdatabase()
        if not conn:
            return "Error: Unable to connect to the database."
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM special")
        spl_scholarships = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template(
            "spl-scholarship.html", spl_scholarships=spl_scholarships
        )
    except Exception as e:
        print("Error fetching all scholarships:", e)
        return "Error: Unable to retrieve data."


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
