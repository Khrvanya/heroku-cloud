from providers.mysql import db
from dataclasses import dataclass

@dataclass
class User(db.Model):
    id: int
    first_name: str
    last_name: str
    birth_year: str

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)