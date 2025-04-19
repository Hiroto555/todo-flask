from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

DB_PATH = Path("todo.db")
app = Flask(__name__)

# データベース接続の設定
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 結果を辞書型として取得
    return conn

# ホームページ（タスク一覧）
@app.route("/")
def index():
    with get_db() as db:
        tasks = db.execute("SELECT id, title, done FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)

# タスク追加
@app.post("/add")
def add():
    title = request.form["title"]
    with get_db() as db:
        db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        db.commit()
    return redirect(url_for("index"))

# タスク完了状態を更新
@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    with get_db() as db:
        db.execute("UPDATE tasks SET done = NOT done WHERE id = ?", (task_id,))
        db.commit()
    return redirect(url_for("index"))

# タスク削除
@app.post("/delete/<int:task_id>")
def delete(task_id):
    with get_db() as db:
        db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        db.commit()
    return redirect(url_for("index"))

# アプリの初期化
if __name__ == "__main__":
    DB_PATH.touch(exist_ok=True)  # データベースファイルが存在しない場合は作成
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER DEFAULT 0  -- 0 = 未完了, 1 = 完了
            )
        """)
    app.run(debug=True)  # デバッグモードでアプリを実行
