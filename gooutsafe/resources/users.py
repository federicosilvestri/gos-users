from flask import request, jsonify
from connexion import NoContent
from gooutsafe.dao.user_manager import UserManager
from gooutsafe.dao.customer_manager import CustomerManager
from gooutsafe.models.customer import Customer
from gooutsafe.models.operator import Operator
import datetime


def create_customer():
    """This method allows the creation of a new customer

    """
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'Already present'
        }), 200

    user = Customer()
    birthday = datetime.datetime.strptime(post_data.get('birthdate'),
                                          '%Y-%m-%d')
    user.set_email(email)
    user.set_password(password)
    if post_data.get('social_number') != "":
        user.set_social_number(post_data.get('social_number'))
    user.set_firstname(post_data.get('firstname'))
    user.set_lastname(post_data.get('lastname'))
    user.set_birthday(birthday)
    user.set_phone(post_data.get('phone'))
    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201


def create_operator():
    """ This method allows the creation of a new operator
    """
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'Already present'
        }), 200

    user = Operator()
    user.set_email(email)
    user.set_password(password)
    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201


def get_user(user_id):
    """
    Get a user by its current id
    :param user_id: user it
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_user_by_email(user_email):
    """
    Get a user by its current email
    :param user_email: user email
    :return: json response
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_user_by_phone(user_phone):
    """
    Get a user by its current id
    :param user_phone: user it
    :return: json response
    """
    user = UserManager.retrieve_by_phone(user_phone)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200

def get_customer_by_ssn(customer_ssn):
    """
    Get a customer by its current ssn
    :param customer_ssn: customer SSN
    :return: json response
    """
    customer = CustomerManager.retrieve_by_ssn(customer_ssn)
    if customer is None:
        response = {'status': 'Costumer not present'}
        return jsonify(response), 404

    return jsonify(customer.serialize()), 200

def get_customer_by_phone(customer_phone):
    """
    Get a customer by its current phone
    :param customer_ssn: customer telephone number
    :return: json response
    """
    customer = CustomerManager.retrieve_by_phone(customer_phone)
    if customer is None:
        response = {'status': 'Costumer not present'}
        return jsonify(response), 404

    return jsonify(customer.serialize()), 200

def delete_user(user_id):
    """Deletes the data of the user from the database.

    Args:
        user_id (int): takes the unique id as a parameter

    Returns:
        Redirects the view to the home page
    """

    """
    
    WE HAVE TO SEND A MESSAGE TO BROKER;
    USER ID= IS ELIMINATED
    if user is not None and user.type == "operator":
        restaurant = RestaurantManager.retrieve_by_operator_id(id)
        if restaurant is not None:
            RestaurantManager.delete_restaurant(restaurant)
    """

    UserManager.delete_user_by_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }

    return jsonify(response_object), 202


def update_customer(id):
    """This method allows the customer to edit their personal information.

    Args:
        id (int): the univocal id for the customer

    Returns:
        Redirects the view to the personal page of the customer
    """

    if request.method == "PUT":
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        phone = post_data.get('phone')

        user = UserManager.retrieve_by_id(id)
        user.set_email(email)
        user.set_password(password)
        user.set_phone(phone)
        UserManager.update_user(user)

        response_object = {
            'status': 'success',
            'message': 'Updated',
        }

        return jsonify(response_object), 204


def update_operator(id):
    """This method allows the operator to edit their personal information.

    Args:
        id (int): the univocal id for the operator

    Returns:
        Redirects the view to the personal page of the operator
    """
    if request.method == "PUT":
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        user = UserManager.retrieve_by_id(id)
        user.set_email(email)
        user.set_password(password)
        UserManager.update_user(user)

        response_object = {
            'status': 'success',
            'message': 'Updated',
        }

        return jsonify(response_object), 204


def add_social_number(id):
    """Allows the user to insert their SSN.

    Args:
        id (int): the univocal id for the user

    Returns:
        Redirects the view to the personal page of the user
    """
    user = UserManager.retrieve_by_id(id)
    if request.method == "PUT":
        post_data = request.get_json()
        social_number = post_data.get('social_number')
        user.set_social_number(social_number)
        UserManager.update_user(user)

        response_object = {
            'status': 'success',
            'message': 'Added social number',
        }

        return jsonify(response_object), 204