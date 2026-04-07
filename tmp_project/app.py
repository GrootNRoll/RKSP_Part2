import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from db import init_db, insert_log, get_all_logs

app = Flask(__name__)

# Инициализация БД только при запуске, а не при импорте
@app.before_request
def _init_db():
    # Выполняется один раз на старте
    if not hasattr(app, '_db_initialized'):
        init_db()
        app._db_initialized = True

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    name = request.form.get("name", "")
    try:
        insert_log(name.strip())
    except Exception as e:
        return str(e), 400
    return redirect(url_for("index"))

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify([{"name": n, "time": t} for n, t in get_all_logs()])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Запуск на http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)