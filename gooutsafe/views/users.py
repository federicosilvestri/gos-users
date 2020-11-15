from flask import Blueprint, redirect, render_template, request, url_for, flash, make_response, jsonify
from flask_login import (login_user, login_required, current_user)

from gooutsafe.dao.user_manager import UserManager
from gooutsafe.forms import UserForm, LoginForm
from gooutsafe.forms.update_customer import UpdateCustomerForm, AddSocialNumberForm
from gooutsafe.models.customer import Customer
from gooutsafe.models.operator import Operator
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

users = Blueprint('users', __name__)


@users.route('/create_user/<string:type_>', methods=['GET', 'POST'])
def create_user_type(type_):
    """This method allows the creation of a new user into the database

    Args:
        type_ (string): as a parameter takes a string that defines the
        type of the new user

    Returns:
        Redirects the user into his profile page, once he's logged in
    """

    if request.method == 'POST':
        post_data = request.get_json()
        user_type = post_data.get('type')
        email = post_data.get('email')
        password = post_data.get('password')

        searched_user = UserManager.retrieve_by_email(email)
        if searched_user is not None:
            return jsonify ({'status': 'Already present'})

        if user_type == "customer":
            user = Customer()
            birthday = datetime.datetime.strptime(post_data.get('birthdate'), 
                '%m/%d/%Y')

            user.set_firstname(post_data.get('firstname'))
            user.set_lastname(post_data.get('lastname'))
            user.set_birthday(birthday)
            user.set_phone(post_data.get('phone'))
        else:
            user = Operator()

        user.set_email(email)
        user.set_password(password)
        UserManager.create_user(user)
        try:
            auth_token = user.encode_auth_token(user.id)
            responseObject = {
                'type': user.type,
                'id': user.id,
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return jsonify(responseObject), 201

        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return jsonify(responseObject), 401


@users.route('/delete_user/<int:id_>', methods=['GET', 'POST'])
@login_required
def delete_user(id_):
    """Deletes the data of the user from the database.

    Args:
        id_ (int): takes the unique id as a parameter

    Returns:
        Redirects the view to the home page
    """
    if current_user.id == id_:
        user = UserManager.retrieve_by_id(id_)
        if user is not None and user.type == "operator":
            restaurant = RestaurantManager.retrieve_by_operator_id(id_)
            if restaurant is not None:
                RestaurantManager.delete_restaurant(restaurant)
        
        UserManager.delete_user_by_id(id_)
    return redirect(url_for('home.index'))


@users.route('/update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    """This method allows the user to edit their personal information.

    Args:
        id (int): the univocal id for the user

    Returns:
        Redirects the view to the personal page of the user
    """
    user = UserManager.retrieve_by_id(id)
    if user.type == "customer":        
        form = UpdateCustomerForm()
    elif user.type == "operator":
        form = LoginForm()

    if request.method == "POST":
        if form.is_submitted():
            email = form.data['email']
            searched_user = UserManager.retrieve_by_email(email)
            if searched_user is not None and id != searched_user.id:
                flash("Data already present in the database.")
                return render_template('update_customer.html', form=form)

            password = form.data['password']
            user.set_email(email)
            user.set_password(password)

            if user.type == "customer":
                phone = form.data['phone']
                user.set_phone(phone)
                UserManager.update_user(user)

                return redirect(url_for('auth.profile', id=user.id))

            elif user.type == "operator":
                UserManager.update_user(user)
                return redirect(url_for('auth.operator', id=user.id))

    return render_template('update_customer.html', form=form)


@users.route('/add_social_number/<int:id>', methods=['GET', 'POST'])
@login_required
def add_social_number(id):
    """Allows the user to insert their SSN.

    Args:
        id (int): the univocal id for the user

    Returns:
        Redirects the view to the personal page of the user
    """
    social_form = AddSocialNumberForm()
    user = UserManager.retrieve_by_id(id)
    if request.method == "POST":
        if social_form.is_submitted():
            social_number = social_form.data['social_number']
            user.set_social_number(social_number)
            UserManager.update_user(user)
            
    return redirect(url_for('auth.profile', id=user.id))