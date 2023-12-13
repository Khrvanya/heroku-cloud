from datetime import datetime
from providers.mysql import db
from dataclasses import dataclass

@dataclass
class ComputerSession(db.Model):
    id: int
    user_id: int
    computer_id: int
    start_date: str
    end_date: str

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)