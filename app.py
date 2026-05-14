import os

if os.environ.get('ENVIRONMENT') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

import os
import logging
import time
from flask import Flask, request, render_template, redirect, url_for, jsonify
from models import db, LogEntry, AppMetrics
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///equipment_log.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        # Ждём готовности БД (на случай, если PG ещё инициализируется)
        for attempt in range(5):
            try:
                db.create_all()
                if not AppMetrics.query.first():
                    db.session.add(AppMetrics())
                    db.session.commit()
                logger.info("✅ БД успешно инициализирована")
                break
            except Exception as e:
                logger.warning(f"⏳ Попытка подключения к БД {attempt+1}/5: {e}")
                time.sleep(2)
        else:
            logger.error("❌ Не удалось подключиться к БД после 5 попыток")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/save", methods=["POST"])
    def save():
        try:
            name = request.form.get("name", "").strip()
            if not name:
                return "Имя не может быть пустым", 400

            new_log = LogEntry(name=name)
            db.session.add(new_log)

            metrics = AppMetrics.query.first()
            metrics.total_saves += 1

            db.session.commit()
            logger.info(f"✅ Записано: {name} (всего: {metrics.total_saves})")
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Ошибка записи: {str(e)}")
            return f"Внутренняя ошибка сервера: {str(e)}", 500

        return redirect(url_for("index"))

    @app.route("/logs", methods=["GET"])
    def get_logs():
        logs = LogEntry.query.order_by(LogEntry.id.desc()).limit(50).all()
        metrics = AppMetrics.query.first()
        return jsonify({
            "total_saves": metrics.total_saves if metrics else 0,
            "entries": [{"name": l.name, "time": str(l.recorded_at)} for l in logs]
        })

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    logger.info(f"🚀 Запуск на http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)