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
        data = data = {'email': customer.email, 'password': TestAuth.faker.password()}
        assert self.client.post('/login', data=data, follow_redirects=True).status_code == 200
        #login for an operator
        self.login_test_operator()
        #login for non existing customer
        data = {'email': TestAuth.faker.email(), 'password': TestAuth.faker.password()}
        assert self.client.post('/login', data=data, follow_redirects=True).status_code == 200
        #login for an authority
        self.login_test_authority()

    def test_get_relogin(self):
        rv = self.client.get('/relogin')
        assert rv.status_code == 200

    def test_get_profile_another_customer(self):
        customer = self.login_test_customer()
        self.login_test_customer()
        #redirect to your home page if you try to see a profile of another customer (for privacy)
        rv = self.client.get('/profile/'+str(customer.id), follow_redirects=True)
        assert rv.status_code == 200

    def test_get_operator_profile(self):
        #check your profile
        operator = self.login_test_operator()
        rv = self.client.get('operator/'+str(operator.id), follow_redirects=True)
        assert rv.status_code == 200
        #try to check profile of another operator(redirect to your home page)
        self.login_test_operator()
        rv = self.client.get('operator/'+str(operator.id), follow_redirects=True)
        assert rv.status_code == 200

    def test_logout(self):
        self.login_test_customer()
        rv = self.client.get('/logout',follow_redirects=True)
        assert rv.status_code == 200

    def test_auth_profile(self):
        authority = self.login_test_authority()
        rv = self.client.get('/authority/'+str(authority.id)+"/0", follow_redirects=True)
        assert rv.status_code == 200
        self.login_test_authority()
        rv = self.client.get('/authority/'+str(authority.id)+"/0", follow_redirects=True)
        assert rv.status_code == 200

    def test_notifications(self):
        self.login_test_customer()
        rv = self.client.get('/notifications', follow_redirects=True)
        assert rv.status_code == 200
        self.login_test_operator()
        rv = self.client.get('/notifications', follow_redirects=True)
        assert rv.status_code == 200




    
    


