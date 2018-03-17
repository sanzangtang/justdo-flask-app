from app import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.find_by_id(id)


class User(db.Model, UserMixin):

    # tablename 'user' does not work in postgres
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    # use Binary for postgres
    password_hash = db.Column(db.Binary())
    todolist = db.relationship('ToDoList', lazy='dynamic')
    keepdolist = db.relationship('KeepDoList', lazy='dynamic')

    def set_password(self, plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password)

    def verify_password(self, plain_password):
        return bcrypt.check_password_hash(self.password_hash, plain_password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class ToDoList(db.Model):

    __tablename__ = 'todolist'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80))
    status = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        return '<ToDoList {}>'.format(self.task)


class KeepDoList(db.Model):

    __tablename__ = 'keepdolist'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80))
    times = db.Column(db.Integer, default=0)
    created_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_check_point = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    daily_check_status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def split_days(self):
        days = self.times
        return {'thirty': days // 30,
                'seven': days % 30 // 7,
                'one': days % 30 % 7
                }

    def __repr__(self):
        return '<KeepDoList {}>'.format(self.task)
