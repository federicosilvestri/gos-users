import datetime

from sqlalchemy.orm import relationship

from gooutsafe import db


class Like(db.Model):
    __tablename__ = 'Like'

    liker_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'Customer.id',
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    liker = relationship(
        'Customer',
        back_populates='likes'
    )

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'Restaurant.id',
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    restaurant = relationship(
        'Restaurant',
        back_populates='likes'
    )

    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kw):
        super(Like, self).__init__(*args, **kw)
