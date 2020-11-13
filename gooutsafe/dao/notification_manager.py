from gooutsafe.models.notification import Notification
from .manager import Manager
from gooutsafe import db


class NotificationManager(Manager):

    @staticmethod
    def create_notification(notification: Notification):
        Manager.create(notification=notification)
    
    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Notification.query.get(id_)

    @staticmethod
    def retrieve_by_target_user_id(user_id):
        Manager.check_none(user_id=user_id)
        return Notification.query.filter(Notification.target_user_id==user_id).all()

    @staticmethod
    def update_notification(notification: Notification):
        Manager.check_none(notification=notification)
        Manager.update(notification=notification)

    @staticmethod
    def delete_notification(notification: Notification):
        Manager.check_none(notification=notification)
        Manager.delete(notification=notification)

    @staticmethod
    def delete_notification_by_id(id_: int):
        notification = NotificationManager.retrieve_by_id(id_)
        NotificationManager.delete_notification(notification)
