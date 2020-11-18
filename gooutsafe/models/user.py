from werkzeug.security import generate_password_hash, check_password_hash

from gooutsafe import db
import datetime

"""TO BE REMOVED"""
JWT_ISSUER = 'com.zalando.connexion'
JWT_ALGORITHM = 'HS256'
JWT_LIFETIME_SECONDS = 600
JWT_SECRET = 'change_this'
"""----"""


class User(db.Model):
    __tablename__ = 'User'

    SERIALIZE_LIST = ['id', 'email', 'is_active', 'authenticated', 'is_anonymous', 'type']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    password = db.Column(db.Unicode(128))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=True)
    is_anonymous = False
    type = db.Column(db.Unicode(128))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    def is_authenticated(self):
        return self.authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self.authenticated = checked
        return self.authenticated

    def is_lha(self):
        return self.type == 'authority'

    def is_rest_operator(self):
        return self.type == 'operator'

    def is_customer(self):
        return self.type == 'customer'

    # def encode_auth_token(self, user_id):
    #     """
    #     Generates the Auth Token
    #     :return: string
    #     """
    #     try:
    #         payload = {
    #             "iss": JWT_ISSUER,
    #             "iat": datetime.datetime.utcnow(),
    #             "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_LIFETIME_SECONDS),
    #             "sub": str(user_id),
    #         }
    #         return jwt.encode(
    #             payload,
    #             JWT_SECRET,
    #             algorithm=JWT_ALGORITHM
    #         )
    #     except Exception as e:
    #         return e
    #
    # @staticmethod
    # def decode_auth_token(auth_token):
    #     """
    #     Decodes the auth token
    #     :param auth_token:
    #     :return: integer|string
    #     """
    #     try:
    #         return jwt.decode(auth_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    #     except jwt.ExpiredSignatureError:
    #         return 'Signature expired. Please log in again.'
    #     except jwt.InvalidTokenError:
    #         return 'Invalid token. Please log in again.'

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
