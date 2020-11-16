from flask import request, jsonify
from connexion import NoContent
from gooutsafe.dao.user_manager import UserManager
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
        return NoContent, 404

    return jsonify(user.serialize()), 200



def delete_user(id_):
    """Deletes the data of the user from the database.

    Args:
        id_ (int): takes the unique id as a parameter

    Returns:
        Redirects the view to the home page
    """

    user = UserManager.retrieve_by_id(id_)
    if user is not None and user.type == "operator":
        restaurant = RestaurantManager.retrieve_by_operator_id(id_)
        if restaurant is not None:
            RestaurantManager.delete_restaurant(restaurant)

    UserManager.delete_user_by_id(id_)
    return redirect(url_for('home.index'))


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

    # return redirect(url_for('auth.profile', id=user.id))
