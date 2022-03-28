from datetime import datetime
from schoolapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True, default="password")
    full_name = db.Column(db.String(100), unique=False, nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(30), nullable=True)
    tuition_fee = db.Column(db.String(20), nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(20))
    grade = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Integer, nullable=True, default=1)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.full_name}', '{self.email}', '{self.address}')"

