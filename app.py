import mysql.connector
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

app = Flask(__name__)

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

#find scholarships
@app.route("/find", methods=["POST"])
def findscholarship():
    try:
        category = request.form.get("category")
        gender = request.form.get("gender")
        income = request.form.get("income")
        conn = getdatabase()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT ScholarshipName,Details,Eligibility  FROM scholarships WHERE category = %s AND gender = %s AND income = %s""",
            (category, gender, income),
        )
        scholarships = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("home.html", scholarships=scholarships)
    except Exception as e:
        print(e)

@app.route("/allscholarships", methods=["GET"])
def allscholarships():
    try:
        conn = getdatabase()
        if not conn:
            return "Error: Unable to connect to the database."

        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT ScholarshipName, Details, Eligibility FROM scholarships"
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
