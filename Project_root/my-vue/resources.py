from flask_restful import Resource, reqparse, marshal_with, fields,Api
from models import User, Role, Section, Ebook, Request, Review
from flask_security import auth_required, current_user
from flask_security.utils import hash_password, verify_password
from extensions import db, security
from datetime import datetime

api = Api(prefix='/api')

user_fields = {
  'id': fields.Integer,
  'email': fields.String,
  'active': fields.Boolean,
}

class UserAPI(Resource):
  @marshal_with(user_fields)
  def get(self, id=None):
      if id:
          user = User.query.get_or_404(id)
          return user
      return User.query.all()

  @marshal_with(user_fields)
  def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('email', required=True)
      parser.add_argument('password', required=True)
      args = parser.parse_args()

      user = User(email=args['email'], password=hash_password(args['password']))
      db.session.add(user)
      db.session.commit()
      return user, 201

  @marshal_with(user_fields)
  def put(self, id):
      user = User.query.get_or_404(id)
      parser = reqparse.RequestParser()
      parser.add_argument('email')
      parser.add_argument('active', type=bool)
      args = parser.parse_args()

      for key, value in args.items():
          if value is not None:
              setattr(user, key, value)

      db.session.commit()
      return user

  def delete(self, id):
      user = User.query.get_or_404(id)
      db.session.delete(user)
      db.session.commit()
      return '', 204

api.add_resource(UserAPI, '/users', '/users/<int:id>')