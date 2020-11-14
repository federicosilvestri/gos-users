from .model_test import ModelTest
import unittest


class TestOperator(ModelTest):

    @classmethod
    def setUpClass(cls):
        super(TestOperator, cls).setUpClass()

        from gooutsafe.models import operator
        cls.operator = operator

    def test_cust_init(self):
        for i in range(0, 10):
            random_operator = TestOperator.generate_random_operator()
            operator, (email, password, is_active, is_admin, is_anonymous) = random_operator

            self.assertEqual(operator.email, email)
            self.assertEqual(operator.password, password)
            self.assertEqual(operator.is_active, is_active)
            self.assertEqual(operator.authenticated, False)
            self.assertEqual(operator.is_anonymous, is_anonymous)

    @staticmethod
    def assertOperatorsEquals(value, expected):
        t = unittest.FunctionTestCase(TestOperator)
        t.assertEqual(value.email, expected.email)
        t.assertEqual(value.password, expected.password)
        t.assertEqual(value.is_active, expected.is_active)
        t.assertEqual(value.authenticated, False)
        t.assertEqual(value.is_anonymous, expected.is_anonymous)

    @staticmethod
    def generate_random_operator():
        from faker import Faker
        from gooutsafe.models import Operator

        faker = Faker()

        email = faker.email()
        password = faker.password()
        is_active = faker.boolean()
        is_admin = faker.boolean()
        authenticated = faker.boolean()
        is_anonymous = faker.boolean()

        operator = Operator(email=email, password=password,
                            is_active=is_active,
                            is_admin=is_admin,
                            authenticated=authenticated,
                            is_anonymous=is_anonymous
                            )
        return operator, (email, password, is_active, is_admin, is_anonymous)
