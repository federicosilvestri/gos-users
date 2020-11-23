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
        #try to creare an existing costumer
        rv = self.client.post('/customer', json=data)
        assert rv.status_code == 200
        assert rv.json['status'] == 'Already present'
    
    def test_create_operator(self):
        data = {'email': TestUsers.faker.email(), 'password': TestUsers.faker.password()}
        rv = self.client.post('/operator', json=data)
        assert rv.status_code == 201
        #try to creare an existing costumer
        rv = self.client.post('/operator', json=data)
        assert rv.status_code == 200
        assert rv.json['status'] == 'Already present'

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

    def test_get_user_by_id(self):
        #get a non-existent user
        rv = self.client.get('/user/0')
        assert rv.status_code == 404
        #get an existent user
        customer = self.login_test_customer()
        rv = self.client.get('/user/%s' % (str(customer.id)))
        assert rv.status_code == 200

    def test_get_user_by_email(self):
        #get a non-existent user with faked email
        rv = self.client.get('/user_email/%s' % (TestUsers.faker.email()))
        assert rv.status_code == 404
        #get an existent user
        customer = self.login_test_customer()
        rv = self.client.get('/user_email/%s'% (customer.email))
        assert rv.status_code == 200

    def test_get_user_by_phone(self):
        #get a non-existent user with faked email
        rv = self.client.get('/user_phone/%s' % (TestUsers.faker.phone_number()))
        assert rv.status_code == 404
        #get an existent user
        customer = self.login_test_customer()
        rv = self.client.get('/user_phone/%s'% (customer.phone))
        assert rv.status_code == 200
        
    def test_get_user_by_ssn(self):
        #get a non-existent user with faked email
        rv = self.client.get('/user_social_number/%s' % (TestUsers.faker.ssn()))
        assert rv.status_code == 404
        #get an existent user
        customer = self.login_test_customer()
        rv = self.client.get('/user_social_number/%s'% (customer.social_number))
        assert rv.status_code == 200

    def test_mark_customer(self):
        customer = self.login_test_customer()
        customer.set_health_status(status=False)
        rv = self.client.put('/mark_positive/%d' % (customer.id))
        assert rv.status_code == 200


