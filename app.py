from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()

    problems = conn.execute("SELECT * FROM problems").fetchall()

    total = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
    completed = conn.execute("SELECT COUNT(*) FROM problems WHERE completed = 1").fetchone()[0]
    easy = conn.execute("SELECT COUNT(*) FROM problems WHERE difficulty = 'Easy'").fetchone()[0]
    medium = conn.execute("SELECT COUNT(*) FROM problems WHERE difficulty = 'Medium'").fetchone()[0]
    hard = conn.execute("SELECT COUNT(*) FROM problems WHERE difficulty = 'Hard'").fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        problems=problems,
        total=total,
        completed=completed,
        easy=easy,
        medium=medium,
        hard=hard
    )

@app.route("/add", methods=["POST"])
def add_problem():
    title = request.form["title"]
    difficulty = request.form["difficulty"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO problems (title, difficulty) VALUES (?, ?)",
        (title, difficulty)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/complete/<int:id>")
def complete_problem(id):
    conn = get_db_connection()
    conn.execute("UPDATE problems SET completed = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete_problem(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM problems WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
