from datetime import datetime, timedelta

from gooutsafe import celery
from gooutsafe.dao.customer_manager import CustomerManager


def schedule_revert_customer_health_status(customer_id, eta=None):
    if not eta:
        eta = datetime.utcnow() + timedelta(days=14)
    revert_customer_health_status.apply_async(kwargs={"customer_id": customer_id}, eta=eta)


@celery.task
def revert_customer_health_status(customer_id):
    customer = CustomerManager.retrieve_by_id(customer_id)
    if customer:
        customer.set_health_status(False)
        CustomerManager.update_customer(customer=customer)
        return 
    else:
        raise ValueError('Customer does not exist anymore')


def notify_restaurant_owners_about_positive_past_customer(customer_id):
    notify_restaurant_owners_about_positive_past_customer_task.delay(customer_id)

@celery.task
def notify_restaurant_owners_about_positive_past_customer_task(customer_id):
    reservations = ReservationManager.retrieve_by_customer_id_in_last_14_days(customer_id)
    for reservation in reservations:
        restaurant = reservation.restaurant
        owner = restaurant.owner
        notification = Notification(owner.id, customer_id, restaurant.id, reservation.start_time)
        NotificationManager.create_notification(notification=notification)


def notify_restaurant_owners_about_positive_booked_customer(customer_id):
    notify_restaurant_owners_about_positive_booked_customer_task.delay(customer_id)

@celery.task
def notify_restaurant_owners_about_positive_booked_customer_task(customer_id):
    reservations = ReservationManager.retrieve_by_customer_id_in_future(customer_id)
    for reservation in reservations:
        restaurant = reservation.restaurant
        owner = restaurant.owner
        notification = Notification(owner.id, customer_id, restaurant.id, reservation.start_time)
        NotificationManager.create_notification(notification=notification)


def notify_customers_about_positive_contact(customer_id):
    notify_customers_about_positive_contact_task.delay(customer_id)

@celery.task
def notify_customers_about_positive_contact_task(customer_id):
    reservations = ReservationManager.retrieve_by_customer_id_in_last_14_days(customer_id)
    for reservation in reservations:
        contact_reservations = ReservationManager.retrieve_all_contact_reservation_by_id(reservation.id)
        for contact_reservation in contact_reservations:
            restaurant = contact_reservation.restaurant
            notification = Notification(contact_reservation.user_id, customer_id, restaurant.id, reservation.start_time)
            NotificationManager.create_notification(notification=notification)
