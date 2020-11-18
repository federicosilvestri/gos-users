from tests.comm import CommTest


class EventsTest(CommTest):

    def test_event(self):
        from gooutsafe.comm.events import Event
        a = Event()
        self.assertTrue(a is not None)

    def test_customer_deletion(self):
        from gooutsafe.comm.events import CustomerDeletion

        event = CustomerDeletion(1)
        self.assertEqual(event.body['user_id'], 1)
        self.assertTrue(len(event.key) > 0)

    def test_operator_deletion(self):
        from gooutsafe.comm.events import OperatorDeletion

        event = OperatorDeletion(1)
        self.assertEqual(event.body['user_id'], 1)
        self.assertTrue(len(event.key) > 0)

    def test_manager(self):
        from gooutsafe.comm.manager import EventManager

        # just try to send messages
        EventManager.operator_deleted(1)
        EventManager.customer_deleted(1)

