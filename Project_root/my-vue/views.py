from flask import current_app as app, jsonify, render_template, request, send_file, make_response
from flask_security import auth_required, current_user, roles_accepted
from flask_security.utils import hash_password, verify_password
from models import User, Role, Section, Ebook, Request, Review
from extensions import security, db
import os
from datetime import datetime, timedelta
from tasks import create_ebook_csv
from flask_excel import make_response_from_query_sets
from celery.result import AsyncResult


def create_view(app):
    @app.route('/')
    def home():
        return "hi"

    @app.route('/register', methods=['POST'])
    def register():
        input_data = request.get_json()
        email = input_data.get('email')
        password = input_data.get('password')
        role = 'user'

        if not email or not password :
            return jsonify({'message': 'Email and password are required'}), 400

        existing_user = security.datastore.find_user(email=email)
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = hash_password(password)
        role_obj = Role.query.filter_by(name=role).first()

        if not role_obj:
            return jsonify({'message': 'Invalid role'}), 400

        user = security.datastore.create_user(
            email=email,
            password=hashed_password,
            roles=[role_obj],
            active=True,

        )
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201

    @app.route('/login', methods=['POST'])
    def user_login():
        input_data = request.get_json()
        input_email = input_data.get('email')
        input_password = input_data.get('password')

        if not input_email or not input_password:
            return jsonify({'message': 'Email and Password are required.'}), 400
        
        if input_email == 'admin@email.com':
            return jsonify({'message': 'Invalid Email ID'}), 400
        
        user = security.datastore.find_user(email=input_email)

        if user and verify_password(input_password, user.password):
            return jsonify({
                'message': 'Login Successful',
                'token': user.get_auth_token(),
                'role': [role.name for role in user.roles],
                'email': user.email
            })
        return jsonify({'message': 'Invalid Credentials'}), 400

    @app.route('/librarian_dashboard')
    @auth_required('session', 'token')
    def librarian_dashboard():
        return "hello librarian. it's your dashboard"

    @app.route('/user_dashboard')
    @auth_required('session', 'token')
    def user_dashboard():
        return "Welcome to the User Dashboard!"






    @app.route('/statistics', methods=['GET'])
    @auth_required('token')
    @roles_accepted('admin')
    def get_statistics():
        # Active Users: Count of users who are marked as active
        active_users_count = User.query.filter_by(active=True).count()

        # Grant Requests: Count of all requests where status is 'granted'
        grant_requests_count = Request.query.filter_by(status='granted').count()

        # E-books Issued: Count of all requests where date_of_return is still None
        ebooks_issued_count = Request.query.filter(Request.date_of_return.is_(None)).count()

        # E-books Revoked: Count of all requests where status is 'revoked'
        ebooks_revoked_count = Request.query.filter_by(status='revoked').count()

        # Constructing the response dictionary
        statistics = {
            "activeUsers": active_users_count,
            "grantRequests": grant_requests_count,
            "ebooksIssued": ebooks_issued_count,
            "ebooksRevoked": ebooks_revoked_count
        }

        print(active_users_count)

        return jsonify(statistics)

    


    # Add other routes as needed

        # Create a new section
    @app.route('/sections', methods=['POST'])
    @auth_required('token')
    @roles_accepted('admin')
    def create_section():
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name:
            return jsonify({'message': 'Name is required'}), 400

        section = Section(name=name, description=description, date_created=datetime.utcnow())
        db.session.add(section)
        db.session.commit()

        return jsonify({'message': 'Section created successfully', 'section': section.name}), 201

    # Get all sections with their ebooks
    @app.route('/sections', methods=['GET'])
    @auth_required('token')
    def get_sections():
        sections = Section.query.all()
        output = []
        for section in sections:
            ebooks = [{'id': ebook.id, 'name': ebook.name, 'author': ebook.author} for ebook in section.ebook]
            section_data = {
                'id': section.id,
                'name': section.name,
                'description': section.description,
                'date_created': section.date_created,
                'ebooks': ebooks
            }
            output.append(section_data)

        return jsonify({'sections': output}), 200

    # Update a section
    @app.route('/sections/<int:id>', methods=['PUT'])
    @auth_required('token')
    @roles_accepted('admin')
    def update_section(id):
        section = Section.query.get_or_404(id)
        data = request.get_json()

        section.name = data.get('name', section.name)
        section.description = data.get('description', section.description)

        db.session.commit()

        return jsonify({'message': 'Section updated successfully'}), 200

    # Delete a section
    @app.route('/sections/<int:id>', methods=['DELETE'])
    @auth_required('token')
    @roles_accepted('admin')
    def delete_section(id):
        section = Section.query.get_or_404(id)
        db.session.delete(section)
        db.session.commit()

        return jsonify({'message': 'Section deleted successfully'}), 200

    # Create an ebook within a section
    @app.route('/sections/<int:section_id>/ebooks', methods=['POST'])
    @auth_required('token')
    @roles_accepted('admin')
    def create_ebook(section_id):
        section = Section.query.get_or_404(section_id)
        data = request.get_json()

        ebook = Ebook(
            name=data.get('name'),
            content=data.get('content'),
            author=data.get('author'),
            section_id=section.id
        )

        db.session.add(ebook)
        db.session.commit()

        return jsonify({'message': 'Ebook added to section successfully'}), 201

    @app.route('/sections/<int:section_id>/ebooks', methods=['GET'])
    def get_ebooks_by_section(section_id):
        # Logic to retrieve ebooks for the section
        ebooks = Ebook.query.filter_by(section_id=section_id).all()

        output = []
        for ebook in ebooks:
            ebook_data = {
                'id': ebook.id,
                'name': ebook.name,
                'author': ebook.author,
                'content': ebook.content,
                'section_id':section_id
            }
            output.append(ebook_data)

        return jsonify({'ebooks': output}), 200

    # CRUD for ebooks (get, update, delete)
    @app.route('/ebooks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    @auth_required('token')
    @roles_accepted('admin')
    def manage_ebook(id):
        ebook = Ebook.query.get_or_404(id)

        if request.method == 'GET':
            return jsonify({
                'id': ebook.id,
                'name': ebook.name,
                'content': ebook.content,
                'author': ebook.author,
                'section_id': ebook.section_id
            }), 200

        elif request.method == 'PUT':
            data = request.get_json()
            ebook.name = data.get('name', ebook.name)
            ebook.content = data.get('content', ebook.content)
            ebook.author = data.get('author', ebook.author)

            db.session.commit()
            return jsonify({'message': 'Ebook updated successfully'}), 200

        elif request.method == 'DELETE':
            db.session.delete(ebook)
            db.session.commit()
            return jsonify({'message': 'Ebook deleted successfully'}), 200
            

    # user functionalities:

    
    @app.route('/user_details', methods=['GET'])
    @auth_required('token')
    @roles_accepted('user')
    def user_details():
        user = current_user
        if user:
            return jsonify({
                "user": {
                    "email": user.email,
                    "active": user.active,
                    "roles": [role.name for role in user.roles]
                }
            })
        else:
            return jsonify({"message": "User not found"}), 404

    @app.route('/active_requests', methods=['GET'])
    @auth_required('token')
    @roles_accepted('user')
    def active_requests():
        user = current_user
        if user:
            active_requests = Request.query.filter_by(user_id=user.id, status = 'pending').all()
            request_data = [
                {
                    "ebook_id": req.ebook_id,
                    "ebook_name": req.ebook.name,
                    "date_of_request": req.date_of_request,
                    "date_of_return": req.date_of_return,
                    "status": req.status,
                } for req in active_requests
            ]
            return jsonify({"active_requests": request_data})
        else:
            return jsonify({"message": "User not found"}), 404


    @app.route('/ebooks/search', methods=['GET'])
    @auth_required('token')
    @roles_accepted('user')
    def search_ebooks():
        query = request.args.get('query', '')
        
        # Search for e-books
        ebooks = Ebook.query.filter(
            (Ebook.name.ilike(f'%{query}%')) | 
            (Ebook.author.ilike(f'%{query}%'))
        ).all()
        
        # Search for sections (if needed)
        sections = Section.query.filter(
            Section.name.ilike(f'%{query}%')
        ).all()
        
        # Prepare response
        ebook_output = [
            {
                'id': ebook.id,
                'name': ebook.name,
                'author': ebook.author,
                'section_id': ebook.section_id
            }
            for ebook in ebooks
        ]
        
        section_output = [
            {
                'id': section.id,
                'name': section.name,
                'description': section.description,
                'date_created': section.date_created
            }
            for section in sections
        ]

        return jsonify({
            'ebooks': ebook_output,
            'sections': section_output
        }), 200


    @app.route('/mybooks', methods=['GET'])
    @auth_required('token')
    @roles_accepted('user')
    def get_my_books():
        user_id = current_user.id
        issued_books = Request.query.filter_by(user_id=user_id, status='granted').all()

        books = [
            {
                'id': request.ebook.id,
                'ebook_name': request.ebook.name,
                'author': request.ebook.author,
                'date_of_return': request.date_of_return,
                #'feedback': Review.query.filter_by(ebook_id=request.ebook.id, user_id=user_id).first() if Review.query.filter_by(ebook_id=request.ebook.id, user_id=user_id).first() else None
            }
            for request in issued_books
        ]
        return jsonify({'books': books}), 200





    @app.route('/content/<int:ebook_id>', methods=['GET'])
    @auth_required('token')
    @roles_accepted('user')
    def ebook_content(ebook_id):
        ebook = Ebook.query.get(ebook_id)
        if ebook:
            print(f"Found ebook: {ebook.name}")
            return jsonify({
                'ebook': {
                    'name': ebook.name,
                    'author': ebook.author,
                    'content': ebook.content
                }
            })
        else:
            print(f"Ebook with ID {ebook_id} not found")
            return jsonify({"message": "Ebook not found"}), 404



    @app.route('/ebooks/<int:ebook_id>/request', methods=['POST'])
    @auth_required('token')
    @roles_accepted('user')
    def request_ebook(ebook_id):
        user_id = current_user.id
        ebook = Ebook.query.get_or_404(ebook_id)
        
        active_requests = Request.query.filter_by(user_id=user_id, status='active').count()
        if active_requests >= 5:
            return jsonify({"error": "Max 5 active requests allowed."}), 400
        
        new_request = Request(user_id=user_id, ebook_id=ebook_id, date_of_request=datetime.now())
        db.session.add(new_request)
        try:
            db.session.commit()
            return jsonify({"message": "Ebook requested successfully!"})
        except Exception as e:
            db.session.rollback()
            print(f"Error committing to the database: {e}")
            return jsonify({"error": "An error occurred while requesting the ebook."}), 500

    @app.route('/requests/<int:request_id>/return', methods=['POST'])
    @auth_required('token')
    @roles_accepted('user')
    def return_ebook(request_id):
        request = Request.query.get_or_404(request_id)
        request.status = 'returned'
        request.date_of_return = datetime.now()
        db.session.commit()
        return jsonify({"message": "Ebook returned successfully!"})


    @app.route('/ebooks/<int:ebook_id>/review', methods=['POST'])
    @auth_required('token')
    @roles_accepted('user')
    def submit_review(ebook_id):
        data = request.get_json()
        new_review = Review(
            feedback=data['feedback'], rating=data.get('rating'),
            user_id=current_user.id, ebook_id=ebook_id
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review submitted!"})




        #handling requests

    @app.route('/requests', methods=['GET'])
    @auth_required('token')
    @roles_accepted('admin')
    def view_requests():
        requests = Request.query.all()
        requests_data = []
        for request in requests:
            requests_data.append({
                'id': request.id,
                'user_id': request.user_id,
                'ebook_id': request.ebook_id,
                'status': request.status,
                'date_requested': request.date_of_request
            })
        return jsonify({'requests': requests_data}), 200

    @app.route('/requests/<int:request_id>/grant', methods=['POST'])
    @auth_required('token')
    @roles_accepted('admin')
    def grant_request(request_id):
        request = Request.query.get_or_404(request_id)
        if request.status != 'pending':
            return jsonify({'message': 'Request is already processed'}), 400

        # Logic to grant the e-book
        request.status = 'granted'
        db.session.commit()
        return jsonify({'message': 'E-book granted successfully'}), 200


    @app.route('/requests/<int:request_id>/revoke', methods=['POST'])
    @auth_required('token')
    @roles_accepted('admin')
    def revoke_request(request_id):
        request = Request.query.get_or_404(request_id)
        if request.status != 'granted':
            return jsonify({'message': 'Cannot revoke a non-granted request'}), 400

        # Logic to revoke the e-book
        request.status = 'revoked'
        db.session.commit()
        return jsonify({'message': 'E-book revoked successfully'}), 200





    return app  