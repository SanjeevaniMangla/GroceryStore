from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from application.models.booking import Booking
from application.models.rating import Rating
from application.models.category import Category
from application.decorator import admin_required

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..models.user import User
from ..models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..parser.categoryParser import category_parser
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import time


def popularity_of_products(category_id):
    # Retrieve the theater
    category = Category.query.get(category_id)

    # Access all shows for the theater
    products = category.products_under_category

    # Calculate total number of tickets sold for each show
    for product in products:
        bookings = Booking.query.filter(Booking.product_id == product.id, Booking.category_id == category.id).all()
        total_products_sold = sum(booking.number_of_products for booking in bookings)
        product.total_products_sold = total_products_sold

    # Sort products based on total products sold in descending order
    sorted_products = sorted(products, key=lambda x: x.total_products_sold, reverse=True)

    # Consider only the top 5 shows
    top_5_items_by_prodcts_sold = sorted_products[:5]
    return top_5_items_by_prodcts_sold

def calculate_average_rating(ratings):
    total_rating = sum(rating.rating for rating in ratings)
    total_users = len(ratings)
    
    if total_users == 0:
        return 0
    
    return total_rating / total_users


def ratings_of_products(category_id):
    # Retrieve the theater
    category = Category.query.get(category_id)

    # Access all shows for the theater
    products = category.products_under_category

    # Calculate average ratings for each show
    for product in products:
        ratings = Rating.query.filter(Rating.product_id == product.id, Rating.category_id == category.id).all()
        average_rating = calculate_average_rating(ratings)
        product.average_rating = average_rating

    # Sort products based on average ratings in descending order
    sorted_products = sorted(products, key=lambda x: x.average_rating, reverse=True)

    # Consider only the top 5 shows
    top_5_products = sorted_products[:5]
    return top_5_products

def price_for_products(category_id):
    # Retrieve the theater
    category = Category.query.get(category_id)

    # Access all shows for the theater
    products = category.products_under_category

    # Calculate total price for each show
    for product in products:
        bookings = Booking.query.filter(Booking.product_id == product.id, Booking.category_id == category.id).all()
        total_price = sum(booking.total_price for booking in bookings)
        product.total_price = total_price

    # Sort shows based on total price in descending order
    sorted_products = sorted(products, key=lambda x: x.total_price, reverse=True)

    # Consider only the top 5 shows
    top_5_products_by_total_price = sorted_products[:5]
    return top_5_products_by_total_price


def create_bar_chart(data, x_labels, parameter_name, file_name):
    plt.bar(x_labels, data)
    plt.xlabel('Products')
    plt.ylabel(parameter_name)
    plt.title(f'Top 5 Products by {parameter_name}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_name)  # Save the figure to a file
    plt.close()

def summary_chart(category_id):
    top_items_by_products_sold = popularity_of_products(category_id)
    top_items_by_average_rating = ratings_of_products(category_id)
    top_items_by_total_price = price_for_products(category_id)
    
    # Extract show names and parameter values for plotting
    product_names = [product.storedName for product in top_items_by_products_sold]
    products_sold = [product.total_products_sold for product in top_items_by_products_sold]
    average_ratings = [product.average_rating for product in top_items_by_average_rating]
    total_prices = [product.total_price for product in top_items_by_total_price]
    
    # Create bar charts for each comparison
    create_bar_chart(products_sold, product_names, 'Number of Products Sold', f'src/assets/summary/category_{category_id}_products_sold.png')
    create_bar_chart(average_ratings, product_names, 'Average Rating', f'src/assets/summary/category_{category_id}_average_ratings.png')
    create_bar_chart(total_prices, product_names, 'Total Price', f'src/assets/summary/category_total_prices.png')


class SummaryAPI(Resource):

    @jwt_required()
    @admin_required
    def get(self, user_id = None, category_id = None):
        summary_chart(category_id)
        time.sleep(5)
        return make_response(jsonify({"message":"Successfully retrieved"}), 200)