from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from gooutsafe.dao.customer_manager import CustomerManager


@authority.route('/ha/mark_positive/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def mark_positive(customer_id):
    """Through this method the health authority can set the health status
    of a specific user to "positive".

    Args:
        customer_id ([int]): univocal id of the user

    Returns:
        Redirects the view to the health authority's home page
    """
    if current_user is not None and current_user.type == 'authority':
        if request.method == 'POST':
            customer = CustomerManager.retrieve_by_id(id_=customer_id)
            if customer is not None and customer.health_status:
                flash("Customer is already set to positive!")
            elif customer is not None:
                customer.set_health_status(status=True)
                CustomerManager.update_customer(customer.id)
                schedule_revert_customer_health_status(customer.id)
                notify_restaurant_owners_about_positive_past_customer(customer.id)
                notify_restaurant_owners_about_positive_booked_customer(customer.id)
                notify_customers_about_positive_contact(customer.id)
                flash("Customer set to positive!")
    return redirect(url_for('auth.authority', id=current_user.id, positive_id=0))


@authority.route('/ha/contact/<int:contact_id>', methods=['GET'])
@login_required
def contact_tracing(contact_id):
    """This method allows the health authority to retrieve the list of
    contacts, given a positive user

    Args:
        contact_id (id): univocal id of the user

    Returns:
        Redirects the view to the health authority's home page
    """
    if current_user is not None and current_user.type == 'authority':
        customer = CustomerManager.retrieve_by_id(id_=contact_id)
        if customer is not None:
            pos_reservations = ReservationManager.retrieve_by_customer_id(user_id=customer.id)
            cust_contacts = []
            restaurant_contacts = []
            date_contacts = []
            for res in pos_reservations:
                contacts = ReservationManager.retrieve_all_contact_reservation_by_id(res.id)
                for c in contacts:
                    cust = CustomerManager.retrieve_by_id(c.user_id)
                    cust_contacts.append(cust)
                    restaurant_contacts.append(RestaurantManager.retrieve_by_id(c.restaurant_id).name)
                    date_contacts.append(c.start_time.date())
            return render_template('contact_tracing_positive.html', customer=customer, pos_contact=cust_contacts,
                                   res_contact=restaurant_contacts, date_contact=date_contacts)
        else:
            return redirect(url_for('auth.authority', id=current_user.id, positive_id=0))
    else:
        return redirect(url_for('home.index'))
