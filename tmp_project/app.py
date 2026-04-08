import os

if os.environ.get('ENVIRONMENT') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

from flask import Flask, request, render_template, redirect, url_for, jsonify
from db import init_db, insert_log, get_all_logs

settings = Dynaconf(
    settings_files=['settings.yaml'],
    environments=True,
    envvar_prefix="EQTEST",  # переменные окружения будут с префиксом EQTEST_
    load_dotenv=True
)

app = Flask(__name__)

app.config['PORT'] = int(os.environ.get('PORT', 5000))
app.config['DEBUG_MODE'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
app.config['DB_PATH'] = os.environ.get('DB_PATH', 'equipment_log.db')

# Инициализация БД только при запуске, а не при импорте
@app.before_request
def _init_db_once():
    if not hasattr(app, '_db_initialized'):
        from db import init_db
        init_db(settings.get('DB_PATH'))
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
    port = settings.get('PORT', 5000)
    debug = settings.get('DEBUG_MODE', False)
    print(f"🚀 Запуск: PORT={port}, DEBUG={debug}, ENV={settings.current_env}")
    app.run(host="0.0.0.0", port=port, debug=debug)