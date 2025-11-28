from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "regilearn_secret_key")

# --------------------------------------------------------
#  MySQL Database Connection (use env vars for flexibility)
# --------------------------------------------------------
try:
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql-service"),   # Kubernetes service name
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "2005"),
        database=os.getenv("MYSQL_DATABASE", "student_db"),
        port=int(os.getenv("MYSQL_PORT", "3306"))
    )
    cursor = db.cursor(dictionary=True)
    print("✅ Connected to MySQL Database")
except mysql.connector.Error as err:
    raise RuntimeError(f"❌ MySQL connection failed: {err}")

# --------------------------------------------------------
#  Index Page
# --------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# --------------------------------------------------------
#  Register Page
# --------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        course = request.form.get("course")
        password = request.form.get("password")

        if not all([name, email, department, course, password]):
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
            print("❌ Error inserting data:", err)
            return "Error saving data."

    return render_template("register.html")

# --------------------------------------------------------
#  Login Page
# --------------------------------------------------------
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
            print("❌ Login error:", err)
            return "Error during login."

    return render_template("login.html")

# --------------------------------------------------------
#  Dashboard
# --------------------------------------------------------
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

# --------------------------------------------------------
#  Logout
# --------------------------------------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# --------------------------------------------------------
#  Courses Page
# --------------------------------------------------------
@app.route("/courses")
def courses():
    return render_template("courses.html")

# --------------------------------------------------------
#  Test Endpoint
# --------------------------------------------------------
@app.route("/test")
def test():
    return "Flask is working fine!"

# --------------------------------------------------------
#  Run Flask Server
# --------------------------------------------------------
if __name__ == "__main__":   # ✅ fixed entrypoint
    app.run(host="0.0.0.0", port=5000, debug=True)