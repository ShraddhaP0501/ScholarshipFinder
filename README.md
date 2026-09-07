🎓 ScholarshipFinder

ScholarshipFinder is a web-based application that helps students find and explore scholarship opportunities based on eligibility criteria such as category, gender, income, course, and academic performance.  
The project is built using **HTML, CSS, and JavaScript** for the frontend, **Flask (Python)** for the backend, and **MySQL** as the database.

🧠 How It Works
1. Frontend (HTML, CSS, JavaScript):
   - Provides a simple and user-friendly interface.
   - Students can select filters such as category, income, gender, and course.
   - Sends user inputs to the backend using HTTP requests.
2. Backend (Flask – Python):
   - Receives filter data from the frontend.
   - Processes requests and queries the MySQL database.
   - Returns matching scholarship details to the frontend.
3. Database (MySQL):
   - Stores scholarship data including eligibility criteria, details, and application links.
   - Enables fast and structured retrieval of scholarship information.

🚀 Features
🔍 Search scholarships based on eligibility
🎯 Filter by category, gender, income, course, and academic performance
📄 View complete scholarship details
🔗 Direct scholarship application links
👤 User-friendly and responsive design
🛠 Admin/User support for adding scholarship data (if implemented)

🛠️ Tech Stack
Frontend
- HTML
- CSS
- JavaScript
Backend
- Python
- Flask
Database
- MySQL

📁 Project Structure
ScholarshipFinder/
│
├── static/ # CSS, JavaScript, images
├── templates/ # HTML templates
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── database.sql # MySQL database schema (if included)
└── README.md

💻 Installation & Setup
🔹 Prerequisites
- Python 3.8+
- MySQL
- pip

🔹 Backend Setup
1. Clone the repository:
   bash
   git clone https://github.com/ShraddhaP0501/ScholarshipFinder.git
   cd ScholarshipFinder
2.Install Python dependencies:
   pip install -r requirements.txt
3.Configure MySQL database:
   Create a database (example: scholarship_db)
   Import database.sql (if available)
   Update database credentials in app.py
4.Run the Flask app:
   python app.py
