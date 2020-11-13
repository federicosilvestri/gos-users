import unittest
from datetime import datetime

from faker import Faker

from .model_test import ModelTest


class TestCustomer(ModelTest):

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestCustomer, cls).setUpClass()
        from gooutsafe.models import customer
        cls.customer = customer

    def test_cust_init(self):
        for i in range(0, 10):
            customer, (name, surname, password, email, birthdate, social_number, health_status, phone) = TestCustomer.generate_random_customer()

            self.assertEqual(customer.email, email)
            self.assertEqual(customer.firstname, name)
            self.assertEqual(customer.lastname, surname)
            self.assertEqual(customer.birthdate, birthdate)
            self.assertEqual(customer.social_number, social_number)
            self.assertEqual(customer.health_status, health_status)
            self.assertEqual(customer.phone, phone)

    @staticmethod
    def assertEqualCustomers(c1, c2):
        t = unittest.FunctionTestCase(TestCustomer)
        t.assertEqual(c1.firstname, c2.firstname)
        t.assertEqual(c1.lastname, c2.lastname)
        t.assertEqual(c1.birthdate, c2.birthdate)
        t.assertEqual(c1.social_number, c2.social_number)
        t.assertEqual(c1.health_status, c2.health_status)
        t.assertEqual(c1.phone, c2.phone)

    @staticmethod
    def generate_random_customer():
        import datetime
        from datetime import date

        from gooutsafe.models import Customer


        complete_name = TestCustomer.faker.name().split(' ')
        name, surname = complete_name[::len(complete_name) - 1]
        password = TestCustomer.faker.password()
        email = TestCustomer.faker.email()
        birthdate = TestCustomer.faker.date_of_birth()
        social_number = TestCustomer.faker.ssn()
        health_status = TestCustomer.faker.boolean()
        phone = TestCustomer.faker.phone_number()
        

        customer = Customer(
            firstname=name,
            lastname=surname,
            email=email,
            password=password,
            birthdate=birthdate,
            social_number=social_number,
            health_status=health_status,
            phone=phone
        )

        return customer, (name, surname, password, email, birthdate, social_number, health_status, phone)

    def test_valid_social_number(self):
        customer, _ = TestCustomer.generate_random_customer()
        social_number = TestCustomer.faker.ssn()
        customer.set_social_number(social_number)
        self.assertEqual(customer.social_number, social_number)

    def test_invalid_social_number(self):
        customer, _ = TestCustomer.generate_random_customer()
        social_number = ''.join(['%s' % i for i in range(0, self.customer.Customer.SOCIAL_CODE_LENGTH + 1)])
        with self.assertRaises(ValueError):
            customer.set_social_number(social_number)
    
    def test_valid_phone(self):
        phone = TestCustomer.faker.phone_number()
        customer, _ = TestCustomer.generate_random_customer()
        customer.set_phone(phone)
        self.assertEqual(customer.phone, phone)

    def test_too_high_phone1(self):
        customer, _ = TestCustomer.generate_random_customer()

        phone = ''.join(['%s' % i for i in range(0, self.customer.Customer.MAX_PHONE_LEN + 1)])
        with self.assertRaises(ValueError):
            customer.set_phone(phone)

    def test_too_short_phone(self):
        customer, _ = TestCustomer.generate_random_customer()
        with self.assertRaises(ValueError):
            phone = ""
            customer.set_phone(phone)

    def test_set_last_notification_read_time(self):
        customer, _ = TestCustomer.generate_random_customer()
        read_time = TestCustomer.faker.date_time()
        customer.set_last_notification_read_time(read_time)
        self.assertEqual(read_time, customer.last_notification_read_time)
