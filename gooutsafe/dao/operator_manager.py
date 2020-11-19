from gooutsafe.models.operator import Operator
from .manager import Manager
from gooutsafe.comm.manager import EventManager


class OperatorManager(Manager):

    @staticmethod
    def create_operator(operator: Operator):
        Manager.create(operator=operator)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Operator.query.get(id_)

    @staticmethod
    def update_operator(operator: Operator):
        Manager.update(operator=operator)

    @staticmethod
    def delete_operator(operator: Operator):
        Manager.delete(operator=operator)
        # trigger the event
        EventManager.operator_deleted(operator.id)

    @staticmethod
    def delete_operator_by_id(id_):
        operator = OperatorManager.retrieve_by_id(id_)
        OperatorManager.delete_operator(operator)
