from .view_test import ViewTest
from faker import Faker


class TestAuth(ViewTest):

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestAuth, cls).setUpClass()

    def test_login(self):
        #login for a customer
        customer = self.login_test_customer()
        #login with a wrong email
        data = {'email': customer.email, 'password': TestAuth.faker.password()}
        response = self.client.post('/authenticate', json=data)
        json_response = response.json
        assert response.status_code == 401
        assert json_response["authentication"] == 'failure'
        assert json_response['user'] is None
        #login for an operator
        self.login_test_operator()
        #login for non existing customer
        data = {'email': TestAuth.faker.email(), 'password': TestAuth.faker.password()}
        response = self.client.post('/authenticate', json=data)
        json_response = response.json
        assert response.status_code == 401
        assert json_response["authentication"] == 'failure'
        assert json_response['user'] is None
        #login for an authority
        self.login_test_authority()

    def test_notifications(self):
        self.login_test_customer()
        rv = self.client.get('/notifications', follow_redirects=True)
        assert rv.status_code == 200
        self.login_test_operator()
        rv = self.client.get('/notifications', follow_redirects=True)
        assert rv.status_code == 200




    
    


