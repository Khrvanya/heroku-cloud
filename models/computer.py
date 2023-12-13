from providers.mysql import db
from dataclasses import dataclass

@dataclass
class Computer(db.Model):
    id: int
    description: str
    price: float

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=False)