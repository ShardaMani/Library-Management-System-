from flask_security import SQLAlchemySessionUserDatastore
from extensions import db
from flask_security.utils import hash_password
from datetime import datetime


def create_data(user_datastore: SQLAlchemySessionUserDatastore):
    print("Creating roles and users")  # For debug purposes

    # Create Roles
    user_datastore.find_or_create_role(name='admin', description='Admin Role')
    user_datastore.find_or_create_role(name='user', description='User Role')

    # Create Users
    if not user_datastore.find_user(email='sharda@gmail.com'):
        user_datastore.create_user(
            email='sharda@gmail.com',
            password=hash_password('sharda'),
            active=True,
            roles=['admin'],
        )

    if not user_datastore.find_user(email='sharda1@gmail.com'):
        user_datastore.create_user(
            email='sharda1@gmail.com',
            password=hash_password('sharda1'),
            active=True,
            roles=['user'],
        )

    if not user_datastore.find_user(email='sharda2@gmail.com'):
        user_datastore.create_user(
            email='sharda2@gmail.com',
            password=hash_password('sharda2'),
            active=True,
            roles=['user'],
        )

    db.session.commit()

    print("######## Data Created ###########")
