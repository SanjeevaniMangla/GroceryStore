from datetime import datetime, timedelta
from jinja2 import Template
from application.models.booking import Booking
from application.models.rating import Rating
from application.models.product import Product
from application.models.category import Category
from weasyprint import HTML
from application.models.user import User
from sqlalchemy import extract

def generate_pdf_report(user, entertainment_data):
    with open("report_template_pdf.html", 'r') as h:
        temp = Template(h.read())
        html_content = temp.render(name = user, data = entertainment_data)
    pdf_file = HTML(string=html_content, base_url="http://localhost:5000").write_pdf()
    return pdf_file


def get_summary_purchase_data(user_id):
    from application import db
    summary_purchase_data =  {
        'total_bookings': 0,
        'total_products': 0,
        'total_products_purchased': 0,
        'total_categories_visited': 0,
        'nummber_of_ratings_given' : 0,
    }
    purchase_data =  summary_purchase_data(user_id)
    summary_purchase_data["total_bookings"] = len(purchase_data["bookings"]) or 0
    summary_purchase_data["total_products"] = sum(booking["number_of_products"] for booking in purchase_data["bookings"]) or 0
    summary_purchase_data["total_products_purchased"] = len(purchase_data["products"]) or 0
    summary_purchase_data["total_categories_visited"] = len(purchase_data["categories"]) or 0
    summary_purchase_data["nummber_of_ratings_given"] = len(purchase_data["ratings"]) or 0

    return summary_purchase_data



def get_purchase_data(user_id):
    purchase_data = {
        "bookings": [],
        "products": [],
        "categories": [],
        "ratings": []
    }
    
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    # Get bookings done by the user in the previous month
    bookings_done_by_user = Booking.query.filter(
        Booking.user_id == user_id,
        extract('year', Booking.created_date_time) == first_day_of_previous_month.year,
        extract('month', Booking.created_date_time) == first_day_of_previous_month.month
    ).all()

    # Get shows seen by the user in the previous month
    products_purchased_in_previous_month = Product.query.filter(
        extract('year', Product.date) == first_day_of_previous_month.year,
        extract('month', Product.date) == first_day_of_previous_month.month
    ).all()

    # Check each show to see if it was booked by the user previously
    for product in products_purchased_in_previous_month:
        # Check if the show was booked by the user earlier
        if Booking.query.filter_by(user_id=user_id, show_id=product.id).first():
            # Add show to the report if it was booked by the user earlier
            purchase_data["products"].append(product)

    # Get theaters to consider
    categories_to_consider = set()
    for product in purchase_data["products"]:
        for category in product.categories:
            # Check if there is any booking for this theatre made by the user in the previous month
            if Booking.query.filter(Booking.theatre_id == category.id, Booking.user_id == user_id).first():
                categories_to_consider.add(category)

    # Fetch distinct shows based on show_ids
    products = purchase_data["products"]
    for index, product in enumerate(products, start=1):
        product.serial_no = index

    # Fetch distinct theatres to consider
    for index, category in enumerate(categories_to_consider, start=1):
        category.serial_no = index
        purchase_data["categories"].append(category)

    # Fill bookings data in the entertainment_data
    
    for index, booking in enumerate(bookings_done_by_user, start=1):
        product = Product.query.get(booking.product_id)
        category = Category.query.get(booking.theatre_id)

        if product and category:
            purchase_data["bookings"].append({
                "serial_no": index,
                "number_of_products": booking.number_of_products,
                "total_price": booking.total_price,
                "product_name": product.storedName,
                "category_name": category.storedName,
                "date_time": booking.created_date_time
            })

    ratings_given_by_user = Rating.query.filter(
        Rating.user_id == user_id,
        extract('year', Rating.created_date_time) == first_day_of_previous_month.year,
        extract('month', Rating.created_date_time) == first_day_of_previous_month.month
    ).all()

    for index, rating in enumerate(ratings_given_by_user, start=1):
        product = Product.query.get(rating.show_id)
        category = Category.query.get(rating.theatre_id)

        if product and category:
            purchase_data["ratings"].append({
                "serial_no": index,
                "rating": rating.rating,
                "product_name": product.storedName,
                "category_name": category.storedName
            })

    return purchase_data