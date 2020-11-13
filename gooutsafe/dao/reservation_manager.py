from gooutsafe.models.reservation import Reservation
from .manager import Manager
from gooutsafe import db
from datetime import datetime, timedelta


class ReservationManager(Manager):

    @staticmethod
    def create_reservation(reservation: Reservation):
        Manager.create(reservation=reservation)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Reservation.query.get(id_)

    @staticmethod
    def retrieve_by_restaurant_id(restaurant_id):
        Manager.check_none(restaurant_id=restaurant_id)
        return Reservation.query.filter(Reservation.restaurant_id==restaurant_id).all()

    @staticmethod
    def retrieve_by_customer_id(user_id):
        Manager.check_none(user_id=user_id)
        return Reservation.query.filter(Reservation.user_id==user_id).all()
    
    @staticmethod
    def retrieve_by_customer_id_in_last_14_days(user_id):
        Manager.check_none(user_id=user_id)
        cond1 = db.and_(Reservation.user_id==user_id, Reservation.end_time >= (datetime.utcnow() - timedelta(days=14)))
        cond2 = db.and_(cond1, Reservation.start_time <= datetime.utcnow())
        return Reservation.query.filter(cond2).all()
    
    @staticmethod
    def retrieve_by_customer_id_in_future(user_id):
        Manager.check_none(user_id=user_id)
        cond = db.and_(Reservation.user_id==user_id, Reservation.start_time > datetime.utcnow())
        return Reservation.query.filter(cond).all()

    @staticmethod
    def retrieve_all_contact_reservation_by_id(id_):
        Manager.check_none(id=id_)
        pos_reservation = ReservationManager.retrieve_by_id(id_)
        cond1 = db.and_(Reservation.start_time <= pos_reservation.start_time, pos_reservation.start_time < Reservation.end_time)
        cond2 = db.and_(Reservation.start_time < pos_reservation.end_time, pos_reservation.end_time < Reservation.end_time)
        cond3 = db.or_(cond1,cond2)
        cond4 = db.and_(cond3, Reservation.restaurant_id==pos_reservation.restaurant_id)
        cond5 = db.and_(cond4, Reservation.user_id!=pos_reservation.user_id, Reservation.start_time < datetime.today() ) #discard the reservations for the same positive customer
        return Reservation.query.filter(cond5).all()

    @staticmethod
    def retrieve_by_table_id(table_id):
        Manager.check_none(table_id=table_id)
        return Reservation.query.filter(Reservation.table_id==table_id).all()

    @staticmethod
    def retrieve_by_date_and_time(restaurant_id, start_time, end_time):
        Manager.check_none(restaurant_id=restaurant_id)
        Manager.check_none(start_time=start_time)
        Manager.check_none(end_time=end_time)
        
        cond1 = db.and_(Reservation.start_time >= start_time, Reservation.start_time < end_time)
        cond2 = db.and_(Reservation.end_time > start_time, Reservation.end_time <= end_time)
        cond3 = db.or_(cond1,cond2)
        cond4 = db.and_(cond3, Reservation.restaurant_id==restaurant_id)
        return Reservation.query.filter(cond4).all()

    @staticmethod
    def update_reservation(reservation: Reservation):
        Manager.check_none(reservation=reservation)
        Manager.update(reservation=reservation)

    @staticmethod
    def delete_reservation(reservation: Reservation):
        Manager.check_none(reservation=reservation)
        Manager.delete(reservation=reservation)

    @staticmethod
    def delete_reservation_by_id(id_: int):
        reservation = ReservationManager.retrieve_by_id(id_)
        ReservationManager.delete_reservation(reservation)
