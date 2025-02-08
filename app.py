import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)


def getdatabase():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1", user="root", password="root", database="scholarshipfinder"
        )
        return conn
    except Exception as e:
        print(e)

@app.route("/")
def home():
    return render_template("index.html")


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
        return render_template("index.html", scholarships=scholarships)
    except Exception as e:
        print(e)
@app.route("/allscholarships", methods=["GET"])
def allscholarships():
    try:
        conn = getdatabase()
        if not conn:
            return "Error: Unable to connect to the database."

        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ScholarshipName, Details, Eligibility FROM scholarships")
        all_scholarships = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template("index2.html", all_scholarships=all_scholarships)

    except Exception as e:
        print("Error fetching all scholarships:", e)
        return "Error: Unable to retrieve data."  


if __name__ == "__main__":
    app.run(debug=True)
