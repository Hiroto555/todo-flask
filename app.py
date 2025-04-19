from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

DB_PATH = Path("todo.db")
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    with get_db() as db:
        tasks = db.execute("SELECT id, title FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)

@app.post("/add")
def add():
    title = request.form["title"]
    with get_db() as db:
        db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        db.commit()
    return redirect(url_for("index"))

@app.post("/delete/<int:task_id>")
def delete(task_id):
    with get_db() as db:
        db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        db.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    DB_PATH.touch(exist_ok=True)
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        """)
    app.run(debug=True)
