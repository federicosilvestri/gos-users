from faker import Faker

from .dao_test import DaoTest


class TestUserManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestUserManager, cls).setUpClass()
        from tests.models.test_user import TestUser
        cls.test_user = TestUser
        from gooutsafe.dao import user_manager
        cls.user_manager = user_manager.UserManager

    def test_crud(self):
        for _ in range(0, 10):
            user = self.test_user.generate_random_user()
            self.user_manager.create_user(user=user)
            user1 = self.user_manager.retrieve_by_id(user.id)
            self.test_user.assertUserEquals(user1, user)
            user.set_password(self.faker.password())
            user.email = self.faker.email()
            self.user_manager.update_user(user=user)
            user1 = self.user_manager.retrieve_by_id(user.id)
            self.test_user.assertUserEquals(user1, user)
            self.user_manager.delete_user(user=user)

    def test_retried_by_email(self):
        base_user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=base_user)
        retrieved_user = self.user_manager.retrieve_by_email(email=base_user.email)
        self.test_user.assertUserEquals(base_user, retrieved_user)
