from datetime import datetime, timedelta
import os
import time
from celery import shared_task
from jinja2 import Template
from application.models.booking import Booking
from application.models.product import Product
from application.models.category import Category
from application.models.user import User
from application.models.rating import Rating
from application.email_send import send_email
from application.pdf_generator import generate_pdf_report, get_purchase_data, get_summary_purchase_data
from main import celery
from flask_weasyprint import HTML
from celery.schedules import crontab
from csv import excel


@celery.task()
def generate_csv(category_id, category_name, products_under_category):

    import csv 
    time.sleep(5)
    
    fields = ['Category ID', 'Category Name', 'Product ID', 'Product Name', 'Total Products', 'Bookings', 'Average Rating', 'No of Ratings Given'] 
        
    current_file_path = os.path.abspath(__file__)
    project_folder_path = os.path.dirname(current_file_path)
    src_folder_path = os.path.join(project_folder_path, 'static')

    filename = os.path.join(src_folder_path, "data.csv")
        
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
        
        for product in products_under_category:
            product_id = product["id"]
            product_name = product["storedName"]
            
            bookings = Booking.query.filter_by(category_id=category_id, product_id=product_id).all()
            ratings = Rating.query.filter_by(category_id=category_id, product_id=product_id).all()
            total_products = sum(booking.number_of_products for booking in bookings)
            total_ratings = sum(rating.rating  for rating in ratings )
            average_rating = 0.0
            if len(ratings) != 0:
                average_rating = (total_ratings / (len(ratings)))
            csvwriter.writerow([category_id, category_name, product_id, product_name, total_products, len(bookings), average_rating, len(ratings)])

    return "Job started..."


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(30.0, send_email_reminder.s(), name="daily reminder")
    sender.add_periodic_task(crontab(day_of_month='12', hour='19', minute='16'), send_monthly_report.s(), name="monthly report")



@celery.task()
def send_email_reminder():
    # Get the list of users who haven't visited the website in the last 24 hours
    # You can query your database for this information
    users_to_remind = get_users_to_remind()

    # Send email reminders to each user in the list
    for user in users_to_remind:

        with open("mail.html", 'r') as h:
            temp=Template(h.read())
            send_email(user.stored_email, subject="Daily Reminder",message=temp.render(name=user))
    
        

def get_users_to_remind():
    # Calculate the datetime 24 hours ago from the current time
    last_24_hours = datetime.now() - timedelta(minutes=2)
    

    # Query the database for users whose last_login is older than 24 hours
    users_to_remind = User.query.filter(User.last_visited < last_24_hours).all()
    

    return users_to_remind


@celery.task()
def send_monthly_report():
    users_to_send_montly_report = get_users_to_send_montly_report()
    for user in users_to_send_montly_report:
        purchase_data = {}
        purchase_data = get_purchase_data(user.id)
        if user.report_format == "HTML":
            with open("report_html.html", 'r') as h:
                temp=Template(h.read())
                html_content = temp.render(name=user, data = purchase_data)
                send_email(user.stored_email, subject="Monthly Purchase Report",message=html_content)
        else:
            with open("report_pdf.html", 'r') as h:
                temp=Template(h.read())
                summary_purchase_data = get_summary_purchase_data(user.id)
                html_content = temp.render(name=user, data = summary_purchase_data)
                pdf_file = generate_pdf_report(user ,purchase_data)
                send_email(user.stored_email, subject="Monthly Purchase Report",message=html_content, attachment=pdf_file, attachment_name="report.pdf" )



def get_users_to_send_montly_report():
    users_to_send_montly_report = User.query.filter(User.role_id==1).all()
    return users_to_send_montly_report
