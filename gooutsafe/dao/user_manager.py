from gooutsafe.dao.manager import Manager
from gooutsafe.models.user import User


class UserManager(Manager):

    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return User.query.get(id_)

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.delete_user(user)
