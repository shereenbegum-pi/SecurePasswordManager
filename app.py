from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "anything_you_like"
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match"

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                  (fullname, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()

        conn.close()

        if user:
            session["user"] = user[1]  # fullname
            return redirect("/dashboard")

        return "Invalid login"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")
@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']

        passwords.append({
            'website': website,
            'username': username,
            'password': password
        })

        return redirect('/dashboard')

    return render_template('add_password.html')

if __name__ == '__main__':
    app.run(debug=True)