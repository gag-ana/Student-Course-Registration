from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import time
import socket

app = Flask(__name__)
app.secret_key = "regilearn_secret_key"

# ✅ MySQL connection with retry + correct port type
def connect_to_database():
    for attempt in range(5):  # retry 5 times
        try:
            print(f"🔁 Attempting to connect to MySQL (try {attempt + 1}/5)...")

            # Check host reachability (for Docker)
            try:
                socket.create_connection(("mysql-service", 3306), timeout=5)
                print("✅ MySQL host reachable.")
            except Exception as e:
                print("⚠️ MySQL host not reachable yet:", e)

            db_conn = mysql.connector.connect(
                host="mysql-service",  # Change to "localhost" if running locally
                user="root",
                password="2005",
                database="student_db",
                port=int(3306)
            )
            print("✅ Connected to MySQL Database")
            return db_conn
        except mysql.connector.Error as err:
            print(f"❌ MySQL connection failed: {err}")
            time.sleep(3)  # wait before retry
    return None

# Initialize DB
db = connect_to_database()
cursor = db.cursor(dictionary=True) if db else None

# 🏠 Home
@app.route("/")
def index():
    return render_template("index.html")

# 🔐 Login
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
                session["user"] = user["name"]
                return redirect(url_for("dashboard"))
            else:
                return "Invalid credentials."
        except mysql.connector.Error as err:
            print("Login error:", err)
            return "Error during login."

    return render_template("login.html")

# 🧑‍🎓 Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"<h2>Welcome, {session['user']}!</h2><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for("login"))

# 🚪 Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# 📝 Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("fullname")
        email = request.form.get("email")
        department = request.form.get("department")
        password = request.form.get("password")

        if not all([name, email, department, password]):
            return "All fields are required!"

        password_hash = generate_password_hash(password)

        try:
            sql = "INSERT INTO users (name, email, department, password_hash) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, department, password_hash))
            db.commit()
            return f"""
            <h2>Registration Successful!</h2>
            <p>Name: {name}</p>
            <p>Email: {email}</p>
            <p>Department: {department}</p>
            <br>
            <a href="/login">Login Now</a> | <a href="/">⬅ Back to Home</a>
            """
        except mysql.connector.Error as err:
            print("Error inserting data:", err)
            return "Error saving data."

    return render_template("register.html")

# 📘 Courses
@app.route("/courses")
def courses():
    return render_template("courses.html")

# 🧪 Test
@app.route("/test")
def test():
    return "Flask is working fine!"

# 🚀 Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)