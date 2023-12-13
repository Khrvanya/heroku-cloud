from server import app
from providers.mysql import db

if __name__ == '__main__':
    # Create tables if not exist
    with app.app_context():
        db.create_all()
        
    app.run(host='127.0.0.1')