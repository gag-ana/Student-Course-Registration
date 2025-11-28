from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import requests

app = Flask(__name__)
app.secret_key = "regilearn_secret_key"

try:
    db = mysql.connector.connect(
        host="mysql-service",
        user="root",
        password="2005",
        database="student_db",
        port=3306
    )
    cursor = db.cursor(dictionary=True)
    print("Connected to MySQL Database")
except mysql.connector.Error as err:
    raise RuntimeError(f"MySQL connection failed: {err}")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        course = request.form.get("course")
        password = request.form.get("password")

        if not name or not email or not department or not course or not password:
            return "All fields are required!"

        password_hash = generate_password_hash(password)

        try:
            sql = """
                INSERT INTO users (name, email, department, course, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, department, course, password_hash))
            db.commit()
            return f"""
            <h2>Registration Successful!</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Department:</strong> {department}</p>
            <p><strong>Course:</strong> {course}</p>
            <br>
            <a href="/login">Login Now</a> | <a href="/">⬅ Back to Home</a>
            """
        except mysql.connector.Error as err:
            print("Error inserting data:", err)
            return "Error saving data."

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Email and password are required."

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session["user"] = {
                    "name": user["name"],
                    "department": user["department"],
                    "course": user["course"]
                }
                return redirect(url_for("dashboard"))
            else:
                return "Invalid credentials."
        except mysql.connector.Error as err:
            print("Login error:", err)
            return "Error during login."

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user = session["user"]
        return f"""
        <h2>Welcome, {user['name']}!</h2>
        <p><strong>Department:</strong> {user['department']}</p>
        <p><strong>Course:</strong> {user['course']}</p>
        <a href='/logout'>Logout</a>
        """
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/test")
def test():
    return "Flask is working fine!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)