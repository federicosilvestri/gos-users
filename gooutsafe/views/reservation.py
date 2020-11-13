from datetime import datetime
from datetime import timedelta

from flask import Blueprint, redirect, render_template, request, url_for, flash
# from flask_user import roles_required
from flask_login import current_user
from flask_login import login_required

from gooutsafe.dao.customer_manager import CustomerManager
from gooutsafe.dao.reservation_manager import ReservationManager
from gooutsafe.dao.restaurant_manager import RestaurantManager
from gooutsafe.dao.table_manager import TableManager
from gooutsafe.forms.filter_form import FilterForm
from gooutsafe.forms.reservation import ReservationForm
from gooutsafe.models.reservation import Reservation
from gooutsafe.models.restaurant import Restaurant
from gooutsafe.models.table import Table

reservation = Blueprint('reservation', __name__)

@reservation.route('/create_reservation/<restaurant_id>', methods=['GET', 'POST'])
@login_required
def create_reservation(restaurant_id):
    """This method allows the customer to create a new reservation, on a specific restaurant,
    depending on its opening hours and the available tables

    Args:
        restaurant_id (int): univocal identifier of the restaurant
    
    """
    if current_user.type == 'customer':
        form = ReservationForm()
        restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
        if request.method == 'POST':
            if form.validate_on_submit():
                start_date = form.data['start_date']
                start_time = form.data['start_time']
                people_number = form.data['people_number']
                start_time_merged = datetime.combine(start_date, start_time)
                table = validate_reservation(restaurant, start_time_merged, people_number)
                if table != False:
                    reservation = Reservation(current_user, table, restaurant, people_number, start_time_merged)
                    ReservationManager.create_reservation(reservation)
                    return redirect(url_for('reservation.customer_my_reservation'))
                else:
                    flash("There aren't free tables for that hour or the restaurant is close")
            else:
                flash("Take a look to the inserted data")
        return render_template('create_reservation.html', restaurant=restaurant, form=form)
    return redirect(url_for('home.index'))


def validate_reservation(restaurant, start_datetime, people_number):
    """
    This method checks if the new reservation overlap with other already 
    present for the restaurant.
    Args:
        restaurant (Restaurant): the reservation restaurant
        start_datetime (datetime): the datetime of the reservation
        people_number (Integer): number of people declered in the reservation

    Returns:
        Teble, Boolean: false in case there are overlap or a table if the restaurant is open and there aren't overlap
    """
    avg_stay = restaurant.avg_stay
    if avg_stay is None:
        end_datetime = start_datetime + timedelta(hours = 3)
    else:
        h_avg_stay = avg_stay//60
        m_avg_stay = avg_stay - (h_avg_stay*60)
        end_datetime = start_datetime + timedelta(hours=h_avg_stay, minutes=m_avg_stay)
    print(start_datetime)
    print(end_datetime)
    if check_rest_ava(restaurant, start_datetime, end_datetime):
        tables = TableManager.retrieve_by_restaurant_id(restaurant.id).order_by(Table.capacity)
        for table in tables:
            if table.capacity >= people_number:
                reservation_table = table
                table_reservations = ReservationManager.retrieve_by_table_id(table_id=table.id)
                if len(table_reservations) != 0:
                    for r in table_reservations:
                        old_start_datetime = r.start_time
                        old_end_datetime = r.end_time
                        print(old_start_datetime)
                        print(old_end_datetime)
                        if start_datetime.date() == old_start_datetime.date():
                            if check_time_interval(start_datetime.time(), end_datetime.time(),
                                                   old_start_datetime.time(), old_end_datetime.time()):
                                continue
                            else:
                                return reservation_table
                        else:
                            return reservation_table
                else:
                    return reservation_table
            else:
                continue
    return False


def check_rest_ava(restaurant, start_datetime, end_datetime):
    """
    This method check if the reservation datetime fall in the retaurant opening hours
    
    Args:
        restaurant (Restaurant): the restaurant in whitch we are booking
        start_datetime (datetime): reservation datetime 
        end_datetime (datetime): reservation end datetime

    Returns:
        [Boolean]: True if the restaurant is open or False if the restaurant is close
    """
    availabilities = restaurant.availabilities
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for ava in availabilities:
        ava_day = ava.day
        res_day = week_days[start_datetime.weekday()]
        if ava_day == res_day:
            if check_time_interval(start_datetime.time(), end_datetime.time(), ava.start_time, ava.end_time):
                return True
    return False


def check_time_interval(start_time1, end_time1, start_time2, end_time2):
    """
    This method check if start_time1 and end_time1 overlap
    the intervall between startime2 and end_time2

    Args:
        start_time1 (datetime)
        end_time1 (datetime)
        start_time2 (datetime)
        end_time2 (datetime)

    Returns:
        Boolean
    """
    if start_time1 >= start_time2 and start_time1 < end_time2:
        return True
    elif end_time1 > start_time2 and end_time1 <= end_time2:
        return True
    return False


@reservation.route('/delete/<int:id>/<restaurant_id>')
def delete_reservation(id, restaurant_id):
    """This method deletes a specific reservation for a restaurant

    Args:
        id (int): univocal identifier of the reservation
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        Redirects the view to the general page of the reservation
    """
    ReservationManager.delete_reservation_by_id(id)
    return redirect(url_for('reservation.reservation_all', restaurant_id=restaurant_id))


@reservation.route('/reservations/<restaurant_id>/<reservation_id>', methods=['GET', 'POST'])
def reservation_details(restaurant_id, reservation_id):
    """ Given a restaurant, this method returns all its reservations

    Args:
        restaurant_id (int): univocal identifier of the restaurant
        reservation_id (int): univocal identifier of the reservations

    Returns:
        [type]: [description]
    """
    reservation = ReservationManager.retrieve_by_id(reservation_id)
    user = CustomerManager.retrieve_by_id(reservation.user.id)
    table = reservation.table
    restaurant = reservation.restaurant
    return render_template("reservation_details.html", reservation=reservation,
                           user=user, table=table, restaurant=restaurant)


@reservation.route('/reservations/<restaurant_id>', methods=['GET', 'POST'])
@login_required
def reservation_all(restaurant_id):
    """Returns the whole list of reservations, given a restaurant.
    It also gives to the operator the opportunity to filter reservations
    by date, so it's possible to count people.

    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        The template of the reservations.
    """
    filter_form = FilterForm()
    reservations = ReservationManager.retrieve_by_restaurant_id(restaurant_id)
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    people = 0
    for r in reservations:
        if r.is_confirmed:
            people = people + r.people_number

    if request.method == 'POST':
        if filter_form.is_submitted():
            filter_date = filter_form.data['filter_date']
            start_time = filter_form.data['start_time']
            end_time = filter_form.data['end_time']

            if filter_date is not None and start_time is not None and end_time is not None:
                start_date_time = datetime.combine(filter_date, start_time)
                end_date_time = datetime.combine(filter_date, end_time)
                res = ReservationManager.retrieve_by_date_and_time(
                    restaurant_id, start_date_time, end_date_time
                )
                people = 0
                for r in res:
                    if r.is_confirmed:
                        people = people + r.people_number

                return render_template("restaurant_reservation.html",
                                       restaurant=restaurant, reservations=res,
                                       filter_form=filter_form, people=people)
            else:
                flash("The form is not correct")
    reservations.sort(key=lambda reservation: reservation.start_time)
    return render_template("restaurant_reservation.html",
                           restaurant=restaurant, reservations=reservations,
                           filter_form=filter_form, people=people)


@reservation.route('/delete/<int:id>/<int:customer_id>', methods=['GET', 'POST'])
def delete_reservation_customer(id, customer_id):
    """Given a customer and a reservation id,
    this function delete the reservation from the database.

    Args:
        id (int): univocal identifier for the reservation

    Returns:
        Redirects the view to the customer profile page.
    """
    ReservationManager.delete_reservation_by_id(id)
    return redirect(url_for('auth.profile', id=customer_id))


@reservation.route('/edit/<int:reservation_id>/<int:customer_id>', methods=['GET', 'POST'])
def edit_reservation(reservation_id, customer_id):
    """Allows the customer to edit a single reservation,
    if there's an available table within the opening hours
    of the restaurant.

    Args:
        reservation_id (int): univocal identifier of the reservation
        customer_id (int): univocal identifier of the customer

    Returns:
        Redirects the view to the customer profile page.
    """
    form = ReservationForm()
    reservation = ReservationManager.retrieve_by_customer_id(user_id=customer_id)[0]
    restaurant = RestaurantManager.retrieve_by_id(reservation.restaurant_id)

    if request.method == 'POST':
        if form.validate_on_submit():
            start_date = form.data['start_date']
            start_time = form.data['start_time']
            people_number = form.data['people_number']
            start_time_merged = datetime.combine(start_date, start_time)
            table = validate_reservation(restaurant, start_time_merged, people_number)
            if table != False:
                reservation.set_people_number(people_number)
                reservation.set_start_time(start_time_merged)
                reservation.set_table(table)
                ReservationManager.update_reservation(reservation)
            else:
                flash("There aren't free tables for that hour or the restaurant is closed")
        else:
            flash("The form is not correct")

    return redirect(url_for('auth.profile', id=customer_id))


@reservation.route('/customer/my_reservations')
def customer_my_reservation():
    """Given the current user, this method returns all its reservations

    """
    form = ReservationForm()
    reservations = ReservationManager.retrieve_by_customer_id(current_user.id)
    reservations.sort(key=lambda reservation: reservation.timestamp, reverse=True)
    return render_template('customer_reservations.html', reservations=reservations, form=form)

@reservation.route('/reservation/confirm/<int:res_id>')
def confirm_reservation(res_id):
    """
    This method is used to confirm reservation

    Args:
        res_id (Integer): the restaurant id of the reservation

    Returns:
        redirect: redirects to the reservations operator page
    """
    reservation = ReservationManager.retrieve_by_id(res_id)
    reservation.set_is_confirmed()
    ReservationManager.update_reservation(reservation)
    return redirect(url_for('reservation.my_reservations'))


@reservation.route('/my_reservations')
def my_reservations():
    """Given a restaurant operator, this method returns all its reservations

    """
    restaurant = RestaurantManager.retrieve_by_operator_id(current_user.id)

    if restaurant is None:
        from gooutsafe.views.restaurants import add
        return add(current_user.id)

    return reservation_all(restaurant.id)
