from gooutsafe import db
from .user import User


class Authority(User):
    __tablename__ = 'Authority'

    id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete="CASCADE"), primary_key=True)
    name = db.Column(db.Unicode(128))
    city = db.Column(db.Unicode(128))
    address = db.Column(db.Unicode(128))
    phone = db.Column(db.Unicode(128))

    __mapper_args__ = {
        'polymorphic_identity': 'authority',
    }

    def __init__(self, *args, **kw):
        super(Authority, self).__init__(*args, **kw)
        self._authenticated = False
