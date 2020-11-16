from .view_test import ViewTest
from faker import Faker
import unittest

class TestHome(ViewTest):

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestHome, cls).setUpClass()

    def test_get_home(self):
        rv = self.client.get('/')    
        assert rv.status_code == 200

    def test_search_restaurant(self):
        #search restaurant with name filter
        data = dict(keyword=TestHome.faker.company(), filters='Name')
        rv = self.client.get('/search', query_string=data)
        assert rv.status_code == 200
        #search restaurant with city filter
        data = dict(keyword=TestHome.faker.city(), filters='City')
        rv = self.client.get('/search', query_string=data)
        assert rv.status_code == 200
        #search restaurant with menu filter
        data = dict(keyword=TestHome.faker.country(), filters='Menu Type')
        rv = self.client.get('/search', query_string=data)
        assert rv.status_code == 200
        #search restaurants with no keyword for the filters
        data = dict(keyword=None, filters='Menu Type')
        rv = self.client.get('/search', query_string=data)
        assert rv.status_code == 200
        #search restaurants with no filters
        data = dict(keyword=TestHome.faker.company(), filters=None)
        rv = self.client.get('/search', query_string=data)
        assert rv.status_code == 200
