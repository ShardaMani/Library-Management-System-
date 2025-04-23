from flask import Flask
from extensions import db, security
from datastorefile import create_data
import os
import resources
from dotenv import load_dotenv
from flask_cors import CORS
from worker import celery_init_app
from config import DevelopmentConfig
from flask_caching import Cache


cache = Cache()




load_dotenv()
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)

  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'Sharda')  # Use environment variable
  app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'Saltypass')  # Use environment variable
  app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'

  app.config.from_object(DevelopmentConfig)


  REDIS_URL = "redis://localhost:6380"

  CORS(app, supports_credentials=True)
  

  cache.init_app(app)
  db.init_app(app)

  


  with app.app_context():
      from views import create_view
      from models import User, Role
      from flask_security import SQLAlchemyUserDatastore
      
      create_view(app)  # Call the function instead of accessing it as a class

      user_datastore = SQLAlchemyUserDatastore(db, User, Role)
      security.init_app(app, user_datastore)

      db.create_all()
      create_data(user_datastore)  # Use the imported function directly
      
  resources.api.init_app(app)

  return app


celery_app = None

if __name__ == '__main__':
  app = create_app()
  celery_app = celery_init_app(app)
  app.run(debug=True)