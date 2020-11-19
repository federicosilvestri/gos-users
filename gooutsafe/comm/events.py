"""
This file contains all events that can be sent as message
to relative channels.
"""


class Event:
    """
    Base event class
    """

    def __init__(self):
        self.key = None
        self.body = None


class CustomerDeletion(Event):
    """
    Class that represents the event "Customer with *id*=id is deleted".
    """

    def __init__(self, user_id):
        self.key = 'CUSTOMER_DELETION'
        self.body = {
            'user_id': user_id
        }


class OperatorDeletion(Event):
    """
    Class that represents the event "Customer with *id*=id is deleted".
    """

    def __init__(self, user_id):
        self.key = 'OPERATOR_DELETION'
        self.body = {
            'user_id': user_id
        }
