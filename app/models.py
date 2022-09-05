from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    links = db.relationship('Link', backref='user', lazy='dynamic')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User: {self.username}'


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    slug = db.Column(db.String(255), index=True, unique=True)
    redirect_url = db.Column(db.String(4096))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    visits = db.relationship('Visit', backref='link', lazy='dynamic')

    def __repr__(self):
        return f'Link: {self.slug}'


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    ip = db.Column(db.String(255), index=True)
    referer = db.Column(db.String(4096))
    user_agent = db.Column(db.String(4096))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'Visit: {self.ip}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
