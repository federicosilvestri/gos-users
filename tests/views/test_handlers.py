from tests.views.view_test import ViewTest
from faker import Faker


class TestHandlers(ViewTest):

    faker = Faker()

    def test_handler_404(self):
        rv = self.client.get('/%s' % self.faker.name())
        assert rv.status_code == 404

    def test_handler_500(self):
        rv = self.client.get('/server_error')
        assert rv.status_code == 500
