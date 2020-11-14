from datetime import datetime

from sqlalchemy.orm import relationship

from gooutsafe import db
from .user import User


class Customer(User):
    SOCIAL_CODE_LENGTH = 16

    __tablename__ = 'Customer'

    MAX_PHONE_LEN = 25

    id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete="CASCADE"), primary_key=True)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    birthdate = db.Column(db.Date)
    social_number = db.Column(db.Unicode(SOCIAL_CODE_LENGTH), default="")
    health_status = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(length=MAX_PHONE_LEN))
    last_notification_read_time = db.Column(db.DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

    def __init__(self, *args, **kw):
        super(Customer, self).__init__(*args, **kw)
        self._authenticated = False

    @staticmethod
    def check_phone_number(phone):
        if len(phone) > Customer.MAX_PHONE_LEN or len(phone) <= 0:
            raise ValueError("Invalid phone number")

    def set_phone(self, phone):
        Customer.check_phone_number(phone)
        self.phone = phone

    def set_firstname(self, name):
        self.firstname = name

    def set_lastname(self, name):
        self.lastname = name

    def set_birthday(self, birthday):
        self.birthdate = birthday

    def set_health_status(self, status):
        self.health_status = status

    @staticmethod
    def check_social_number(social_number):
        if len(social_number) != Customer.SOCIAL_CODE_LENGTH:
            raise ValueError("Invalid Social Number length")

    def set_social_number(self, social_number):
        Customer.check_social_number(social_number)
        self.social_number = social_number

    def set_last_notification_read_time(self, read_time):
        self.last_notification_read_time = read_time

    def new_notifications(self):
        return 0
