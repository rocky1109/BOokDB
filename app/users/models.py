
from app import db
from flask_login import UserMixin

from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(length=80), unique=True, nullable=False)
    access_token = db.Column(db.String(length=80))
    picture = db.Column(db.String(length=250))
    first_name = db.Column(db.String(length=30))
    last_name = db.Column(db.String(length=30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def full_name(self):
        return self.email.split('@')[0] if not (self.first_name or
                                                self.last_name) \
            else "%s %s" % (self.first_name, self.last_name)

    @property
    def username(self):
        return self.email.split('@')[0]

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
