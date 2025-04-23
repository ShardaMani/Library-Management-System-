from extensions import db
from flask_security import UserMixin, RoleMixin
from flask_security.models import fsqla_v3 as fsqla
from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import relationship

fsqla.FsModels.set_db_info(db)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(65), unique=True, nullable=False)

    requests = db.relationship('Request', backref='user', lazy=True)
    roles = db.relationship('Role', secondary='user_roles')
    roles = db.relationship('Role', secondary='roles_users', backref= db.backref('users', lazy='dynamic'))
    @property
    def role(self):
        return [role.name for role in self.roles]


    

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Section(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = True)
    date_created = db.Column(db.Date(), nullable = True)
    description = db.Column(db.String())

    ebook = db.Relationship('Ebook', backref='section',  cascade="all, delete-orphan")


class Ebook(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = True)
    content = db.Column(db.String())
    author = db.Column(db.String(), nullable = False)
    
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable = False)
    request = db.relationship('Request', backref='ebook',  cascade="all, delete-orphan")
    review = db.relationship('Review', backref='ebook',  cascade="all, delete-orphan" )

class Request(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    date_of_request = db.Column(db.Date, nullable = True)
    days_requested = db.Column(db.Integer, nullable = True)
    date_of_return = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(), default='pending')

    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable = False)

class Review(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    feedback = db.Column(db.String(), nullable = False)
    rating = db.Column(db.Integer, nullable = True)

    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable = False)