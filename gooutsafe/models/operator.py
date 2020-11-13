from sqlalchemy.orm import relationship

from gooutsafe import db
from .user import User


class Operator(User):
    __tablename__ = 'Operator'

    id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    restaurant = relationship('Restaurant', uselist=False, back_populates="owner")

    __mapper_args__ = {
        'polymorphic_identity': 'operator',
    }

    def __init__(self, *args, **kw):
        super(Operator, self).__init__(*args, **kw)
        self._authenticated = False

    def set_restaurant(self, restaurant):
        self.restaurant = restaurant

    def new_notifications(self):
        return 0
