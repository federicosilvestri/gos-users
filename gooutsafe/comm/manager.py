from gooutsafe.comm import rabbit, disabled
from gooutsafe import logger
from gooutsafe.comm.events import *


class EventManager(object):
    """This class is the event manager of system.
    It handles all events that application can trigger.

    Each method inside this class will send a message to message broker.
    """

    @classmethod
    def _send_message(cls, event: Event):
        """
        Send a message to broker.

        :param event: event to be sent
        :return: None
        """
        if disabled:
            return

        logger.info('<%s> event triggered, sending message to MB' % event.key)
        rabbit.send(
            body=event.body,
            routing_key=event.key
        )

    @classmethod
    def operator_deleted(cls, user_id):
        """
        Trigger the event user_deleted.

        :param user_id: the id of user
        :return: None
        """
        event = OperatorDeletion(user_id)
        cls._send_message(event)

    @classmethod
    def customer_deleted(cls, user_id):
        """
        Trigger the event user_deleted.

        :param user_id: the id of user
        :return: None
        """
        event = CustomerDeletion(user_id)
        cls._send_message(event)
