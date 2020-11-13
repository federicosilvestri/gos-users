from datetime import datetime, timedelta
from random import randint

from faker import Faker

from .dao_test import DaoTest


class TestReservationManager(DaoTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestReservationManager, cls).setUpClass()

        from tests.models.test_customer import TestCustomer
        cls.test_customer = TestCustomer
        from tests.models.test_reservation import TestReservation
        cls.test_reservation = TestReservation
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant
        from tests.models.test_table import TestTable
        cls.test_table = TestTable
        from tests.models.test_user import TestUser
        cls.test_user = TestUser

        from gooutsafe.dao import reservation_manager
        cls.reservation_manager = reservation_manager.ReservationManager
        from gooutsafe.dao import customer_manager
        cls.customer_manager = customer_manager.CustomerManager
        from gooutsafe.dao import user_manager
        cls.user_manager = user_manager.UserManager
        from gooutsafe.dao import restaurant_manager
        cls.restaurant_manager = restaurant_manager.RestaurantManager        
        from gooutsafe.dao import table_manager
        cls.table_manager = table_manager.TableManager
        from gooutsafe.dao import customer_manager
        cls.customer_manager = customer_manager.CustomerManager
    
    def test_create_reservation(self):
        reservation1, _ = self.test_reservation.generate_random_reservation()
        self.reservation_manager.create_reservation(reservation=reservation1)
        reservation2 = self.reservation_manager.retrieve_by_id(id_=reservation1.id)
        self.test_reservation.assertEqualReservations(reservation1, reservation2)

    def test_delete_reservation(self):
        base_reservation, _ = self.test_reservation.generate_random_reservation()
        self.reservation_manager.create_reservation(reservation=base_reservation)
        self.reservation_manager.delete_reservation(base_reservation)
        self.assertIsNone(self.reservation_manager.retrieve_by_id(base_reservation.id))

    def test_delete_reservation_by_id(self):
        base_reservation, _ = self.test_reservation.generate_random_reservation()
        self.reservation_manager.create_reservation(reservation=base_reservation)
        self.reservation_manager.delete_reservation_by_id(base_reservation.id)
        self.assertIsNone(self.reservation_manager.retrieve_by_id(base_reservation.id))

    def test_update_reservation(self):
        base_reservation, _ = self.test_reservation.generate_random_reservation()
        self.reservation_manager.create_reservation(reservation=base_reservation)
        base_reservation.set_people_number(TestReservationManager.faker.random_int(min=0,max=15))
        start_time = TestReservationManager.faker.date_time_between('now','+6w')
        base_reservation.set_start_time(start_time)
        updated_reservation = self.reservation_manager.retrieve_by_id(id_=base_reservation.id)
        self.test_reservation.assertEqualReservations(base_reservation, updated_reservation)

    def test_retrieve_by_user_id(self):
        reservation, _ = self.test_reservation.generate_random_reservation()
        user = reservation.user
        self.user_manager.create_user(user=user)
        self.reservation_manager.create_reservation(reservation=reservation)
        retrieved_reservation = self.reservation_manager.retrieve_by_customer_id(user_id=user.id)
        for res in retrieved_reservation:
            self.test_reservation.assertEqualReservations(reservation, res)

    def test_retrieve_by_restaurant_id(self):
        reservation, _ = self.test_reservation.generate_random_reservation()
        restaurant = reservation.restaurant
        self.restaurant_manager.create_restaurant(restaurant=restaurant)
        self.reservation_manager.create_reservation(reservation=reservation)
        retrieved_reservation = self.reservation_manager.retrieve_by_restaurant_id(restaurant_id=restaurant.id)
        for res in retrieved_reservation:
            self.test_reservation.assertEqualReservations(reservation, res)
    
    def test_retrieve_by_table_id(self):
        reservation, _ = self.test_reservation.generate_random_reservation()
        table = reservation.table
        self.table_manager.create_table(table=table)
        self.reservation_manager.create_reservation(reservation=reservation)
        retrieved_reservation = self.reservation_manager.retrieve_by_table_id(table_id=table.id)
        for res in retrieved_reservation:
            self.test_reservation.assertEqualReservations(reservation, res)
    
    def test_retrieve_by_customer_id(self):
        reservation, _ = self.test_reservation.generate_random_reservation()
        customer = reservation.user
        self.customer_manager.create_customer(customer=customer)
        self.reservation_manager.create_reservation(reservation=reservation)
        retrieved_reservation = self.reservation_manager.retrieve_by_customer_id(user_id=customer.id)
        for res in retrieved_reservation:
            self.test_reservation.assertEqualReservations(reservation, res)

    def test_single_retrieve_by_customer_id_in_last_14_days(self):
        customer, _ = self.test_customer.generate_random_customer()
        self.customer_manager.create_customer(customer=customer)
        valid_reservation, _ = self.test_reservation.generate_random_reservation(user=customer)
        self.reservation_manager.create_reservation(reservation=valid_reservation)
        invalid_reservation, _ = self.test_reservation.generate_random_reservation(user=customer)
        invalid_reservation.set_start_time(datetime.utcnow() - timedelta(days=randint(15, 100)))
        self.reservation_manager.create_reservation(reservation=invalid_reservation)
        retrieved_reservation = self.reservation_manager.retrieve_by_customer_id_in_last_14_days(user_id=customer.id)
        for res in retrieved_reservation:
            self.test_reservation.assertEqualReservations(valid_reservation, res)

    def test_multiple_retrieve_by_customer_id_in_last_14_days(self):
        customer, _ = self.test_customer.generate_random_customer()
        self.customer_manager.create_customer(customer=customer)
        valid_reservations = []
        for _ in range(randint(2, 10)):
            valid_reservation, _ = self.test_reservation.generate_random_reservation(user=customer, start_time_mode='valid_past_contagion_time')
            self.reservation_manager.create_reservation(reservation=valid_reservation)
            valid_reservations.append(valid_reservation)
        for _ in range(randint(2, 10)):
            invalid_reservation, _ = self.test_reservation.generate_random_reservation(user=customer)
            invalid_reservation.set_start_time(datetime.utcnow() - timedelta(days=randint(15, 100)))
            self.reservation_manager.create_reservation(reservation=invalid_reservation)
        retrieved_reservations = self.reservation_manager.retrieve_by_customer_id_in_last_14_days(user_id=customer.id)
        for retrieved, valid in zip(retrieved_reservations, valid_reservations):
            self.test_reservation.assertEqualReservations(valid, retrieved)

    def test_retrieve_by_customer_id_in_future(self):
        customer, _ = self.test_customer.generate_random_customer()
        self.customer_manager.create_customer(customer=customer)
        valid_reservations = []
        for _ in range(randint(2, 10)):
            valid_reservation, _ = self.test_reservation.generate_random_reservation(user=customer, start_time_mode='valid_future_contagion_time')
            self.reservation_manager.create_reservation(reservation=valid_reservation)
            valid_reservations.append(valid_reservation)
        for _ in range(randint(2, 10)):
            invalid_reservation, _ = self.test_reservation.generate_random_reservation(user=customer)
            invalid_reservation.set_start_time(datetime.utcnow() - timedelta(days=randint(1, 100)))
            self.reservation_manager.create_reservation(reservation=invalid_reservation)
        retrieved_reservations = self.reservation_manager.retrieve_by_customer_id_in_future(user_id=customer.id)
        for retrieved, valid in zip(retrieved_reservations, valid_reservations):
            self.test_reservation.assertEqualReservations(valid, retrieved)

    def test_retrieve_all_contact_reservation_by_id(self):
        from gooutsafe.models.reservation import Reservation
        from gooutsafe.models.table import Table
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant=restaurant)
        start_time_positive = datetime(year=2020, month=11, day=2, hour=11)
        end_time_positive = start_time_positive + timedelta(Reservation.MAX_TIME_RESERVATION)
        contacted_users = []
        for _ in range(0, self.faker.random_int(min=2, max=10)):
            table,_ = self.test_table.generate_random_table(fixed_restaurant=restaurant)
            self.table_manager.create_table(table)
            start_time = datetime(year=2020, month=11, day=2, hour=self.faker.random_int(min=11,max=13), minute=self.faker.random_int(min=0,max=59))
            contacted_user = self.test_user.generate_random_user()
            contacted_users.append(contacted_user)
            self.user_manager.create_user(contacted_user)
            reservation = Reservation(contacted_user, table, restaurant, 1, start_time)
            self.reservation_manager.create_reservation(reservation)

        table1, _= self.test_table.generate_random_table(fixed_restaurant=restaurant)
        positive_user = self.test_user.generate_random_user()
        self.user_manager.create_user(positive_user)
        positive_reservation = Reservation(positive_user, table1, restaurant, 1, start_time_positive)
        self.reservation_manager.create_reservation(positive_reservation)
        retrieved_contacted_reservations = self.reservation_manager.retrieve_all_contact_reservation_by_id(positive_reservation.id)
        retrieved_contacted_users = []
        for res in retrieved_contacted_reservations:
            retrieved_contacted_users.append(res.user)
        retrieved_contacted_users.sort(key=lambda positive_user: positive_user.id)
        contacted_users.sort(key=lambda positive_user: positive_user.id)
        for retrieved_contacted_user, contacted_user in zip(retrieved_contacted_users, contacted_users):
            self.test_user.assertUserEquals(contacted_user, retrieved_contacted_user)

    def test_retrieve_by_date_and_time(self):
        from gooutsafe.models.reservation import Reservation
        from gooutsafe.models.table import Table
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant=restaurant)
        start_interval = datetime(year=2020, month=11, day=30, hour=0)
        end_interval = start_interval + timedelta(hours=23)
        reservations = []
        for i in range(0, self.faker.random_int(min=1, max=10)):
            table,_ = self.test_table.generate_random_table(fixed_restaurant=restaurant)
            self.table_manager.create_table(table)
            start_time = datetime(year=2020, month=11, day=30, hour=i+1)
            user = self.test_user.generate_random_user()
            self.user_manager.create_user(user)
            reservation = Reservation(user, table, restaurant, 1, start_time)
            reservations.append(reservation)
            self.reservation_manager.create_reservation(reservation)
        retreived_res = self.reservation_manager.retrieve_by_date_and_time(restaurant.id, start_interval, end_interval)
        self.assertListEqual(reservations, retreived_res)