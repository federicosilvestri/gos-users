import unittest


class ViewTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    client = None

    @classmethod
    def setUpClass(cls):
        from gooutsafe import create_app
        app = create_app()
        cls.client = app.test_client()
        from tests.models.test_customer import TestCustomer
        cls.test_customer = TestCustomer
        from gooutsafe.dao import customer_manager
        cls.customer_manager = customer_manager.CustomerManager
        from tests.models.test_operator import TestOperator
        cls.test_operator = TestOperator
        from gooutsafe.dao import operator_manager
        cls.operator_manager = operator_manager.OperatorManager
        from tests.models.test_authority import TestAuthority
        cls.test_authority = TestAuthority
        from gooutsafe.dao import health_authority_manager
        cls.authority_manager = health_authority_manager.AuthorityManager

    def login_test_customer(self):
        """
        Simulate the customer login for testing the resources
        :return: customer
        """
        customer, _ = self.test_customer.generate_random_customer()
        psw = customer.password
        customer.set_password(customer.password)
        self.customer_manager.create_customer(customer=customer)
        data = {'email': customer.email, 'password': psw}
        response = self.client.post('/authenticate', json=data)
        json_response = response.json
        assert response.status_code == 200
        assert json_response["authentication"] == 'success'
        assert json_response['user'] is not None

        return customer

    def login_test_operator(self):
        """
        Simulate the operator login for testing the resources
        :return: operator
        """
        operator, _ = self.test_operator.generate_random_operator()
        psw = operator.password
        operator.set_password(operator.password)
        self.operator_manager.create_operator(operator=operator)
        data = {'email': operator.email, 'password': psw}
        response = self.client.post('/authenticate', json=data)
        json_response = response.json
        assert response.status_code == 200
        assert json_response["authentication"] == 'success'
        assert json_response['user'] is not None

        return operator

    def login_test_authority(self):
        """
        Simulate the authority login for testing the resources
        :return: authority
        """
        authority, _ = self.test_authority.generate_random_authority()
        psw = authority.password
        authority.set_password(authority.password)
        self.authority_manager.create_authority(authority=authority)
        data = {'email': authority.email, 'password': psw}
        response = self.client.post('/authenticate', json=data)
        json_response = response.json
        assert response.status_code == 200
        assert json_response["authentication"] == 'success'
        assert json_response['user'] is not None
        
        return authority
