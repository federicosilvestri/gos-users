from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, make_response
from flask_login import (logout_user, login_user, login_required)

from flask_login import current_user
from gooutsafe.dao.customer_manager import CustomerManager
from gooutsafe.dao.health_authority_manager import AuthorityManager
from gooutsafe.dao.user_manager import UserManager
from gooutsafe.forms import LoginForm
from gooutsafe.forms.authority import AuthorityForm
from gooutsafe.forms.update_customer import AddSocialNumberForm
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login(re=False):
    """Allows the user to log into the system

    Args:
        re (bool, optional): boolean value that describes whenever
        the user's session is new or needs to be reloaded. Defaults to False.

    Returns:
        Redirects the view to the personal page of the user
    """
    if request.method == "POST":
        post_data = request.get_json()
        email = post_data.get('email')
        
        try:
            user = UserManager.retrieve_by_email(email)
            if user and check_password_hash(user.password, post_data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode(),
                        'type': user.type,
                        'user_id': user.id
                    }
                    return jsonify(responseObject), 200

        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return jsonify(responseObject), 500


@auth.route('/relogin')
def re_login():
    """Method that is being called after the user's session is expired.

    """
    return login(re=True)


@auth.route('/authority/<int:id>/<int:positive_id>', methods=['GET', 'POST'])
def authority(id, positive_id):
    """This method allows the Health Authority to see its personal page.

    Args:
        id (int): the univocal identifier for the Health Authority
        positive_id (int): the identifier of the positive user

    Returns:
        Redirects to the page of the Health Authority
    """
    """
    if current_user.id == id:
        authority = AuthorityManager.retrieve_by_id(id)
        ha_form = AuthorityForm()
        pos_customers = CustomerManager.retrieve_all_positive()
        search_customer = CustomerManager.retrieve_by_id(positive_id)
        return render_template('authority_profile.html', current_user=authority,
                               form=ha_form, pos_customers=pos_customers, 
                               search_customer=search_customer)"""
    return redirect(url_for('home.index'))


@auth.route('/logout')
@login_required
def logout():
    """This method allows the users to log out of the system

    Returns:
        Redirects the view to the home page
    """
    logout_user()
    return redirect('/')


@auth.route('/notifications', methods=['GET'])
@login_required
def notifications():
    """[summary]

    Returns:
        [type]: [description]
    """
    notifications = NotificationManager.retrieve_by_target_user_id(current_user.id)
    processed_notification_info = []
    if current_user.type == "customer":
        for notification in notifications:
            restaurant_name = RestaurantManager.retrieve_by_id(notification.contagion_restaurant_id).name
            processed_notification_info.append({"timestamp": notification.timestamp,
                                                 "contagion_datetime": notification.contagion_datetime,
                                                 "contagion_restaurant_name": restaurant_name})
        return render_template('customer_notifications.html', current_user=current_user, notifications=processed_notification_info)
    elif current_user.type == "operator":
        for notification in notifications:
            info = {"timestamp": notification.timestamp,
                    "contagion_datetime": notification.contagion_datetime}
            is_future = notification.timestamp < notification.contagion_datetime
            info['is_future'] = is_future
            if is_future:
                customer_phone_number = UserManager.retrieve_by_id(notification.positive_customer_id).phone
                info['customer_phone_number'] = customer_phone_number
            processed_notification_info.append(info)
        return render_template('operator_notifications.html', current_user=current_user, notifications=processed_notification_info)
