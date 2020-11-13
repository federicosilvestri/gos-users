from datetime import datetime
from datetime import timedelta

from sqlalchemy.orm import relationship

from gooutsafe import db


class Reservation(db.Model):
    __tablename__ = 'Reservation'

    MAX_TIME_RESERVATION = 3

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete="CASCADE"))
    user = relationship('User', foreign_keys='Reservation.user_id')
    table_id = db.Column(db.Integer, db.ForeignKey('Table.id', ondelete="CASCADE"))
    table = relationship('Table')
    restaurant_id = db.Column(db.Integer, db.ForeignKey('Restaurant.id'))
    restaurant = relationship("Restaurant", back_populates="reservations")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    people_number = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    is_confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, user, table, restaurant, people_number, start_time):
        self.user = user
        self.table = table
        self.restaurant = restaurant
        self.people_number = people_number
        self.start_time = start_time        
        self.set_end_time_by_avg_stay(restaurant.avg_stay)    

    @staticmethod
    def check_time(start_time, end_time):
        actual_time = datetime.utcnow()
        if start_time >= end_time:
            raise ValueError('The start time cannot be greater than end_time')

    def set_end_time_by_avg_stay(self, avg_stay):
        if avg_stay is None or avg_stay == 0:
            self.end_time = self.start_time + timedelta(hours=self.MAX_TIME_RESERVATION)
        else:
            avg_stay = self.restaurant.avg_stay
            h_avg_stay = avg_stay//60
            m_avg_stay = avg_stay - (h_avg_stay*60)
            self.end_time = self.start_time + timedelta(hours=h_avg_stay, minutes=m_avg_stay)

    def set_user(self, user):
        self.user = user

    def set_table(self, table):
        self.table = table

    def set_restaurant(self, restaurant):
        self.restaurant = restaurant

    def set_people_number(self, people_number):
        self.people_number = people_number

    def set_start_time(self, start_time):
        self.start_time = start_time
        self.set_end_time(start_time + timedelta(hours=self.MAX_TIME_RESERVATION))

    def set_end_time(self, end_time):
        Reservation.check_time(self.start_time, end_time)
        self.end_time = end_time
    
    def set_is_confirmed(self):
        self.is_confirmed = True

