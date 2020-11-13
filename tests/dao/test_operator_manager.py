from faker import Faker

from .dao_test import DaoTest


class TestOperatorManager(DaoTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestOperatorManager, cls).setUpClass()

        from tests.models.test_operator import TestOperator
        cls.test_operator = TestOperator

        from gooutsafe.dao import operator_manager
        cls.operator_manager = operator_manager.OperatorManager
    
    def test_create_operator(self):
        operator1, _ = self.test_operator.generate_random_operator()
        self.operator_manager.create_operator(operator=operator1)
        operator2 = self.operator_manager.retrieve_by_id(id_=operator1.id)
        self.test_operator.assertOperatorsEquals(operator1, operator2)
    
    def test_delete_operator(self):
        base_operator, _ = self.test_operator.generate_random_operator()
        self.operator_manager.create_operator(operator=base_operator)
        self.operator_manager.delete_operator(base_operator)
        self.assertIsNone(self.operator_manager.retrieve_by_id(base_operator.id))

    def test_delete_operator_by_id(self):
        base_operator, _ = self.test_operator.generate_random_operator()
        self.operator_manager.create_operator(operator=base_operator)
        self.operator_manager.delete_operator_by_id(base_operator.id)
        self.assertIsNone(self.operator_manager.retrieve_by_id(base_operator.id))
