from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from app.models import Admin 

with app.app_context():
    db.create_all()  

    admin_exists = Admin.query.filter_by(username='quizmaster').first()

    if not admin_exists:
        admin_user = Admin(username='quizmaster', password='quiz123')
        db.session.add(admin_user)
        db.session.commit()


from app import routes,models
