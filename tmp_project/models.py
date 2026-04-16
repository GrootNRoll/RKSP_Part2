from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class LogEntry(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    recorded_at = db.Column(db.DateTime, server_default=func.now())

class AppMetrics(db.Model):
    __tablename__ = 'metrics'
    id = db.Column(db.Integer, primary_key=True, default=1)
    total_saves = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())