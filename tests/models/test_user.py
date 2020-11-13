import random
import unittest

from faker import Faker

from .model_test import ModelTest


class TestUser(ModelTest):

    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()

        from gooutsafe.models import user
        cls.user = user

    @staticmethod
    def assertUserEquals(value, expected):
        t = unittest.FunctionTestCase(TestUser)
        t.assertEqual(value.email, expected.email)
        t.assertEqual(value.password, expected.password)
        t.assertEqual(value.is_active, expected.is_active)
        t.assertEqual(value.authenticated, False)
        t.assertEqual(value.is_anonymous, expected.is_anonymous)

    @staticmethod
    def generate_random_user():
        email = TestUser.faker.email()
        password = TestUser.faker.password()
        is_active = TestUser.faker.boolean()
        is_admin = TestUser.faker.boolean()
        authenticated = TestUser.faker.boolean()
        is_anonymous = TestUser.faker.boolean()

        from gooutsafe.models import User

        user = User(
            email=email,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
            authenticated=authenticated,
            is_anonymous=is_anonymous,
        )

        return user

    def test_set_password(self):
        user = TestUser.generate_random_user()
        password = self.faker.password(length=10, special_chars=False, upper_case=False)
        user.set_password(password)

        self.assertEqual(
            user.authenticate(password),
            True
        )
    
    def test_set_email(self):
        user = TestUser.generate_random_user()
        email = self.faker.email()
        user.set_email(email)
        self.assertEqual(email, user.email)
    
    """
    def test_authenticate(self):
        user = TestUser.generate_random_user()
        password = self.faker.password(length=10, special_chars=False, upper_case=False)
        user.set_password(generate_password_hash(password))
        self.assertTrue(user.authenticate(generate_password_hash(password)))
    """

    def test_is_authenticated(self):
        user = TestUser.generate_random_user()
        self.assertFalse(user.is_authenticated())

    def test_is_lha(self):
        from .test_authority import TestAuthority
        user,_ = TestAuthority.generate_random_authority()
        self.assertTrue(user.is_lha())

    def test_is_rest_operator(self):
        from .test_operator import TestOperator
        user,_ = TestOperator.generate_random_operator()
        self.assertTrue(user.is_customer)

    def test_is_customer(self):
        from .test_customer import TestCustomer
        user,_ = TestCustomer.generate_random_customer()
        self.assertTrue(user.is_customer)

