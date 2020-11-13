from faker import Faker

from .form_test import FormTest


class TestReservationForm(FormTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestReservationForm, cls).setUpClass()
        from gooutsafe.forms.reservation import ReservationForm
        cls.reservation_form = ReservationForm
        # from models.test_customer import TestCustomer
        # cls.test_customer = TestCustomer
        # from gooutsafe.dao import customer_manager
        # cls.customer_manager = customer_manager.CustomerManager
    
    def test_correct_validate_on_submit(self):
        pass

    def test_failed_validate_on_submit(self):
        pass