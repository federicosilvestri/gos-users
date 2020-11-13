from datetime import datetime, timedelta

from faker import Faker

from .dao_test import DaoTest


class TestNotificationManager(DaoTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestNotificationManager, cls).setUpClass()

        from tests.models.test_notification import TestNotification
        cls.test_notification = TestNotification
        from tests.models.test_user import TestUser
        cls.test_user = TestUser

        from gooutsafe.dao import user_manager
        cls.user_manager = user_manager.UserManager
        from gooutsafe.dao import notification_manager
        cls.notification_manager = notification_manager.NotificationManager

    def test_create_notification(self):
        notification, _ = self.test_notification.generate_random_notification()
        self.notification_manager.create_notification(notification=notification)
        retrieved_notification = self.notification_manager.retrieve_by_id(id_=notification.id)
        self.test_notification.assertEqualNotifications(notification, retrieved_notification)

    def test_update_notification(self):
        notification, _ = self.test_notification.generate_random_notification()
        self.notification_manager.create_notification(notification=notification)
        notification.set_contagion_datetime(TestNotificationManager.faker.date_time())
        self.notification_manager.update_notification(notification=notification)
        retrieved_notification = self.notification_manager.retrieve_by_id(id_=notification.id)
        self.test_notification.assertEqualNotifications(notification, retrieved_notification)

    def test_delete_notification(self):
        notification, _ = self.test_notification.generate_random_notification()
        self.notification_manager.create_notification(notification=notification)
        self.notification_manager.delete_notification(notification=notification)
        self.assertIsNone(self.notification_manager.retrieve_by_id(id_=notification.id))

    def test_delete_notification_by_id(self):
        notification, _ = self.test_notification.generate_random_notification()
        self.notification_manager.create_notification(notification=notification)
        self.notification_manager.delete_notification_by_id(id_=notification.id)
        self.assertIsNone(self.notification_manager.retrieve_by_id(id_=notification.id))
    
    def test_retrieve_notification_by_target_user_id(self):
        target_user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=target_user)
        notification, _ = self.test_notification.generate_random_notification(target_user)
        self.notification_manager.create_notification(notification=notification)
        retrieved_notification = self.notification_manager.retrieve_by_target_user_id(user_id=target_user.id)[0]
        self.test_notification.assertEqualNotifications(notification, retrieved_notification)
