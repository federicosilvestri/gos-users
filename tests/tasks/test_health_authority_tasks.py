from random import randint

from unittest.mock import patch

from .tasks_test import TasksTest


class TestHealthAuthorityTasks(TasksTest):

    @classmethod
    def setUpClass(cls):
        super(TestHealthAuthorityTasks, cls).setUpClass()

        from tests.models.test_authority import TestAuthority
        cls.test_authority = TestAuthority
        from tests.models.test_customer import TestCustomer
        cls.test_customer = TestCustomer
        from tests.models.test_operator import TestOperator
        cls.test_operator = TestOperator
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant
        from tests.models.test_reservation import TestReservation
        cls.test_reservation = TestReservation

        from gooutsafe.dao import health_authority_manager
        cls.health_authority_manager = health_authority_manager.AuthorityManager
        from gooutsafe.dao import customer_manager
        cls.customer_manager = customer_manager.CustomerManager
        from gooutsafe.dao import operator_manager
        cls.operator_manager = operator_manager.OperatorManager
        from gooutsafe.dao import restaurant_manager
        cls.restaurant_manager = restaurant_manager.RestaurantManager
        from gooutsafe.dao import reservation_manager
        cls.reservation_manager = reservation_manager.ReservationManager
        from gooutsafe.dao import notification_manager
        cls.notification_manager = notification_manager.NotificationManager

        from gooutsafe.tasks import health_authority_tasks
        cls.health_authority_tasks = health_authority_tasks


    # def setUpClass(cls):
    #     super(TestHealthAuthorityTasks, self).setUp()

    # def test_schedule_revert_health_status(self):
    #     with patch('gooutsafe.tasks.health_authority_tasks.revert_customer_health_status') as task_mock:
    #         customer, _ = TestCustomer.generate_random_customer()
    #         self.customer_manager.create_customer(customer=customer)
    #         self.health_authority_tasks.schedule_revert_customer_health_status(customer)
    #         assert task_mock.called

    def test_revert_health_status(self):
        # authority, _ = TestAuthority.generate_random_authority()
        # self.health_authority_manager.create_authority(authority=authority)
        customer, _ = self.test_customer.generate_random_customer()
        customer.set_health_status(True)
        self.customer_manager.create_customer(customer=customer)
        customer_id = customer.id
        self.health_authority_tasks.revert_customer_health_status(customer_id)
        customer_retrieved = self.customer_manager.retrieve_by_id(customer_id)
        self.assertEqual(customer_retrieved.health_status, False)

    def test_notify_restaurant_owners_about_positive_past_customer_task(self):
        # create positive customer
        customer, _ = self.test_customer.generate_random_customer()
        customer.set_health_status(True)
        self.customer_manager.create_customer(customer=customer)
        customer_id = customer.id
        notifications_data = []
        for _ in range(randint(2, 10)):
            # create random owners
            operator, _ = self.test_operator.generate_random_operator()
            # create random restaurant for each owner
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            self.operator_manager.create_operator(operator=operator)
            restaurant.owner_id = operator.id
            self.restaurant_manager.create_restaurant(restaurant=restaurant)
            # create random reservation for customer in each restaurant
            reservation, _ = self.test_reservation.generate_random_reservation(user=customer, restaurant=restaurant, start_time_mode='valid_past_contagion_time')
            self.reservation_manager.create_reservation(reservation=reservation)
            notifications_data.append((operator.id, restaurant.id, reservation.id))
        self.health_authority_tasks.notify_restaurant_owners_about_positive_past_customer_task(customer_id)
        # check if notifications are there
        customer = self.customer_manager.retrieve_by_id(customer_id)
        for operator_id, restaurant_id, reservation_id in notifications_data:
            operator = self.operator_manager.retrieve_by_id(operator_id)
            restaurant = self.restaurant_manager.retrieve_by_id(restaurant_id)
            reservation = self.reservation_manager.retrieve_by_id(reservation_id)
            notification = self.notification_manager.retrieve_by_target_user_id(operator.id)[0]
            self.assertEqual(notification.target_user_id, operator.id)
            self.assertEqual(notification.positive_customer_id, customer.id)
            self.assertEqual(notification.contagion_restaurant_id, restaurant.id)
            self.assertEqual(notification.contagion_datetime, reservation.start_time)


    def test_notify_restaurant_owners_about_positive_booked_customer_task(self):
        # create positive customer
        customer, _ = self.test_customer.generate_random_customer()
        customer.set_health_status(True)
        self.customer_manager.create_customer(customer=customer)
        customer_id = customer.id
        notifications_data = []
        for _ in range(randint(2, 10)):
            # create random owners
            operator, _ = self.test_operator.generate_random_operator()
            # create random restaurant for each owner
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            self.operator_manager.create_operator(operator=operator)
            restaurant.owner_id = operator.id
            self.restaurant_manager.create_restaurant(restaurant=restaurant)
            # create random reservation for customer in each restaurant
            reservation, _ = self.test_reservation.generate_random_reservation(user=customer, restaurant=restaurant, start_time_mode='valid_future_contagion_time')
            self.reservation_manager.create_reservation(reservation=reservation)
            notifications_data.append((operator.id, restaurant.id, reservation.id))
        self.health_authority_tasks.notify_restaurant_owners_about_positive_booked_customer_task(customer_id)
        # check if notifications are there
        customer = self.customer_manager.retrieve_by_id(customer_id)
        for operator_id, restaurant_id, reservation_id in notifications_data:
            operator = self.operator_manager.retrieve_by_id(operator_id)
            restaurant = self.restaurant_manager.retrieve_by_id(restaurant_id)
            reservation = self.reservation_manager.retrieve_by_id(reservation_id)
            notification = self.notification_manager.retrieve_by_target_user_id(operator.id)[0]
            self.assertEqual(notification.target_user_id, operator.id)
            self.assertEqual(notification.positive_customer_id, customer.id)
            self.assertEqual(notification.contagion_restaurant_id, restaurant.id)
            self.assertEqual(notification.contagion_datetime, reservation.start_time)

    def test_notify_customers_about_positive_contact_task(self):
        # create positive customer
        positive_customer, _ = self.test_customer.generate_random_customer()
        positive_customer.set_health_status(True)
        self.customer_manager.create_customer(customer=positive_customer)
        positive_customer_id = positive_customer.id
        notifications_data = []
        for _ in range(randint(2, 10)):
            # create random customer
            customer, _ = self.test_customer.generate_random_customer()
            # create random restaurant
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            self.restaurant_manager.create_restaurant(restaurant=restaurant)
            # create random reservation for both positive customer and customer in each restaurant
            reservation1, _ = self.test_reservation.generate_random_reservation(user=customer, restaurant=restaurant, start_time_mode='valid_past_contagion_time')
            reservation2, _ = self.test_reservation.generate_random_reservation(user=positive_customer, restaurant=restaurant)
            reservation2.set_start_time(reservation1.start_time)
            self.reservation_manager.create_reservation(reservation=reservation1)
            self.reservation_manager.create_reservation(reservation=reservation2)
            notifications_data.append((customer.id, restaurant.id, reservation1.id))
        self.health_authority_tasks.notify_customers_about_positive_contact_task(positive_customer_id)
        # check if notifications are there
        positive_customer = self.customer_manager.retrieve_by_id(positive_customer_id)
        for customer_id, restaurant_id, reservation_id in notifications_data:
            customer = self.customer_manager.retrieve_by_id(customer_id)
            restaurant = self.restaurant_manager.retrieve_by_id(restaurant_id)
            reservation = self.reservation_manager.retrieve_by_id(reservation_id)
            notification = self.notification_manager.retrieve_by_target_user_id(customer.id)[0]
            self.assertEqual(notification.target_user_id, customer.id)
            self.assertEqual(notification.positive_customer_id, positive_customer.id)
            self.assertEqual(notification.contagion_restaurant_id, restaurant.id)
            self.assertEqual(notification.contagion_datetime, reservation.start_time)
