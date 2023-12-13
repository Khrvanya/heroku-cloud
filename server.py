from flask import Flask, render_template, request, redirect, url_for, jsonify
from models.user import User
from models.computer import Computer
from models.computer_session import ComputerSession
from providers.mysql import db
from datetime import datetime

app = Flask(__name__)

# Configure databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hu2nomejxeylnvo8:lvev1fb5zoxs64h3@i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com/gn9qnb720ln1pd15'

# Initialize databases
db.init_app(app)

@app.route('/user', methods=['POST'])
def create_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    birth_year = int(request.json['birth_year'])

    user = User(first_name=first_name, last_name=last_name, birth_year=birth_year)
    db.session.add(user)
    db.session.commit()

    return jsonify(user)


@app.route('/user/<int:user_id>', methods=['GET'])
def read_user(user_id):
    user = db.get_or_404(User, {"id": user_id})

    return jsonify(user)


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.get_or_404(User, {"id": user_id})

    user.first_name = request.json['first_name']
    user.last_name = request.json['last_name']
    user.birth_year = int(request.json['birth_year'])
    db.session.commit()

    return jsonify(user)


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    active_computer_sessions = db.session.execute(db.select(ComputerSession).filter_by(user_id=user_id, end_date=None)).scalars().all()
    if len(active_computer_sessions) > 0:
        return "Active computer session for this user exists", 400
    
    user = db.get_or_404(User, {"id": user_id})

    db.session.delete(user)
    db.session.commit()

    return jsonify(id = user.id)


@app.route('/computer', methods=['POST'])
def create_computer():
    description = request.json['description']
    price = float(request.json['price'])

    computer = Computer(description=description, price=price)
    db.session.add(computer)
    db.session.commit()

    return jsonify(computer)


@app.route('/computer/<int:computer_id>', methods=['GET'])
def read_computer(computer_id):
    computer = db.get_or_404(Computer, {"id": computer_id})

    return jsonify(computer)


@app.route('/computer/<int:computer_id>', methods=['PUT'])
def update_computer(computer_id):
    computer = db.get_or_404(Computer, {"id": computer_id})

    computer.description = request.json['description']
    computer.price = float(request.json['price'])
    db.session.commit()

    return jsonify(computer)


@app.route('/computer/<int:computer_id>', methods=['DELETE'])
def delete_computer(computer_id):
    active_computer_sessions = db.session.execute(db.select(ComputerSession).filter_by(computer_id=computer_id, end_date=None)).scalars().all()
    if len(active_computer_sessions) > 0:
        return "Active computer session for this computer exists", 400
        
    computer = db.get_or_404(Computer, {"id": computer_id})
    
    db.session.delete(computer)
    db.session.commit()

    return jsonify(id = computer.id)


@app.route('/computer_session', methods=['POST'])
def create_computer_session():
    computer_id = int(request.json['computer_id'])
    user_id = int(request.json['user_id'])

    user = db.get_or_404(User, {"id": user_id})

    computer = db.get_or_404(Computer, {"id": computer_id})

    computer_session = ComputerSession(computer_id=computer_id, user_id=user_id)
    db.session.add(computer_session)
    db.session.commit()

    return jsonify(computer_session)


@app.route('/computer_session/<int:computer_session_id>', methods=['GET'])
def read_computer_session(computer_session_id):
    computer_session = db.get_or_404(ComputerSession, {"id": computer_session_id})

    return jsonify(computer_session)


@app.route('/computer_session/<int:computer_session_id>/end', methods=['POST'])
def end_computer_session(computer_session_id):
    computer_session = db.get_or_404(ComputerSession, {"id": computer_session_id})
    
    computer_session.end_date = datetime.utcnow()
    db.session.commit()

    return jsonify(computer_session)