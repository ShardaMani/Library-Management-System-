from celery import shared_task
from models import User, Role, Request, Review, Ebook, Section
import flask_excel as excel
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from datetime import datetime, timedelta
from json import dumps
from httplib2 import Http

# SMTP Configuration
SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = 'library.librarian@email.com'
SENDER_PASSWORD = ''

## CSV FILE GENERATING TASK

@shared_task(ignore_result=False)
def create_ebook_csv(user_id):
    user = User.query.get(user_id)
    issued_books = Request.query.filter_by(user_id=user_id).with_entities(
        Request.date_of_request, Request.date_of_return, Ebook.name, Ebook.author
    ).join(Ebook).all()
    
    csv_output = excel.make_response_from_query_sets(
        issued_books, ['date_of_request', 'date_of_return', 'name', 'author'], "csv"
    )
    filename = f'issued_books_{user.name}.csv'

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename

## MAILHOG TASK (MONTHLY REPORT) ##

@shared_task(ignore_result=True)
def send_monthly_activity_report():
    librarian_users = User.query.filter(User.roles.any(Role.name == 'librarian')).all()

    with open('monthly_report_template.html', 'r') as f:
        template = Template(f.read())
        for librarian in librarian_users:
            issued_books = Request.query.filter(Request.date_of_request >= (datetime.utcnow() - timedelta(days=30))).all()
            sections = Section.query.all()
            reviews = Review.query.all()

            send_email(librarian.email, 'Monthly Activity Report', template.render(
                issued_books=issued_books, sections=sections, reviews=reviews
            ))
    
    return "Monthly Activity Report Sent"

def send_email(to, subject, content_body):
    msg = MIMEMultipart()
    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))
    
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()

## WEBHOOK TASK ##

@shared_task(ignore_result=False)
def send_daily_reminders():
    timestamp = datetime.utcnow() + timedelta(days=1)
    approaching_users = User.query.join(Request).filter(
        Request.date_of_return <= timestamp
    ).all()

    if not approaching_users:
        return "No users with approaching return dates today"
    
    for user in approaching_users:
        if user.email:
            send_notification(user.email)
    
    return "Daily reminders sent to users with approaching return dates"

def send_notification(email):
    """Google Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/AAAAPBURMfM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=1pQXlpbg_KGJYBRclS2Z9OyXskd6ROG4e15IihL7nhU"
    app_message = {"text": f"Hello! Your return date is approaching. Please return your borrowed book on time."}
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
