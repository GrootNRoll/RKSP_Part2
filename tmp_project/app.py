from flask import Flask, request, render_template, redirect, url_for, jsonify
from db import init_db
from logic import save_device_event, fetch_device_logs

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET"])
def index():
    # Данные из БД НЕ загружаются при старте страницы
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    name = request.form.get("name", "")
    try:
        save_device_event(name)
    except ValueError as e:
        return str(e), 400
    return redirect(url_for("index"))

# Новый маршрут: отдаёт содержимое БД только по явному запросу
@app.route("/logs", methods=["GET"])
def get_logs():
    logs = fetch_device_logs()
    return jsonify([{"name": name, "time": ts} for name, ts in logs])   