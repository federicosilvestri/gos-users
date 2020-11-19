from .view_test import ViewTest
from faker import Faker
import datetime
import unittest

class TestUsers(ViewTest):

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestUsers, cls).setUpClass()

    def test_create_customer(self):
        social_number = TestUsers.faker.ssn()
        email = TestUsers.faker.email()
        name = 'Charlie'
        surname = 'Brown'
        password = TestUsers.faker.password()
        birthdate = datetime.date(year=1992,month=12,day=12)
        phone = TestUsers.faker.phone_number()
        data = {'email': email, 'password': password, 'social_number': social_number, 'firstname': name, 'lastname': surname, 'birthdate': birthdate, 'phone':phone}
        rv = self.client.post('/customer', json=data)
        assert rv.status_code == 201
    
    def test_create_operator(self):
        data = {'email': TestUsers.faker.email(), 'password': TestUsers.faker.password()}
        rv = self.client.post('/operator', json=data)
        assert rv.status_code == 201

    def test_delete_user(self):
        customer = self.login_test_customer()
        rv = self.client.delete('/user/'+str(customer.id))
        assert rv.status_code == 202
        
    def test_update_customer(self):
        customer = self.login_test_customer()
        data = {'email': TestUsers.faker.email(), 'password': TestUsers.faker.password(), 'phone': TestUsers.faker.phone_number()}
        rv = self.client.put('/customer/'+str(customer.id), json=data)
        assert rv.status_code == 204
        
    def test_update_operator(self):
        operator = self.login_test_operator()
        data = {'email': TestUsers.faker.email(), 'password': TestUsers.faker.password()}
        rv = self.client.put('/operator/'+str(operator.id), json=data)
        assert rv.status_code == 204

    def test_update_ssn(self):
        customer = self.login_test_customer()
        data = {'social_number': TestUsers.faker.ssn()}
        rv = self.client.put('/social_number/'+str(customer.id), json=data)
        assert rv.status_code == 204
