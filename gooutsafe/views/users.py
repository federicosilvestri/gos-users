from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import (login_user, login_required, current_user)

from gooutsafe.dao.restaurant_manager import RestaurantManager
from gooutsafe.dao.user_manager import UserManager
from gooutsafe.forms import UserForm, LoginForm
from gooutsafe.forms.update_customer import UpdateCustomerForm, AddSocialNumberForm
from gooutsafe.models.customer import Customer
from gooutsafe.models.operator import Operator

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
    form = LoginForm()
    if type_ == "customer":
        form = UserForm()
        user = Customer()
    else:
        user = Operator()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.data['email']
            searched_user = UserManager.retrieve_by_email(email)
            if searched_user is not None:
                flash("Data already present in the database.")
                return render_template('create_user.html', form=form)

            form.populate_obj(user)
            user.set_password(form.password.data)

            UserManager.create_user(user)

            login_user(user)
            user.authenticated = True

            if user.type == 'operator':
                return redirect(url_for('auth.operator', id=user.id))
            else:
                return redirect(url_for('auth.profile', id=user.id))
        else:
            for fieldName, errorMessages in form.errors.items():
                for errorMessage in errorMessages:
                    flash('The field %s is incorrect: %s' % (fieldName, errorMessage))

    return render_template('create_user.html', form=form, user_type=type_)


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