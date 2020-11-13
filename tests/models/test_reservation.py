import unittest
from datetime import datetime, timedelta

from faker import Faker

from .model_test import ModelTest


class TestReservation(ModelTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestReservation, cls).setUpClass()

        from gooutsafe.models import reservation, restaurant, table, user

        cls.reservation = reservation
        cls.table = table
        cls.user = user
        cls.restaurant = restaurant

        from .test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant
        from .test_table import TestTable
        cls.test_table = TestTable
        from .test_user import TestUser
        cls.test_user = TestUser

    @staticmethod
    def generate_random_reservation(user=None, restaurant=None, start_time_mode=None):
        from gooutsafe.models.reservation import Reservation
        test_reservation = TestReservation()
        test_reservation.setUpClass()
        if user is None:
            user = test_reservation.test_user.generate_random_user()
        table, _ = test_reservation.test_table.generate_random_table()
        if restaurant is None:
            restaurant, _ = test_reservation.test_restaurant.generate_random_restaurant()
        people_number = test_reservation.faker.random_int(min=0,max=table.MAX_TABLE_CAPACITY)
        if start_time_mode == 'valid_past_contagion_time':
            start_time = test_reservation.faker.date_time_between_dates(datetime.utcnow()-timedelta(days=14), datetime.utcnow())
        elif start_time_mode == 'valid_future_contagion_time':
            start_time = test_reservation.faker.date_time_between('now', '+14d')
        else:
            start_time = TestReservation.faker.date_time_between('now', '+6w')
        reservation = Reservation(
            user = user,
            table = table,
            restaurant = restaurant,
            people_number = people_number,
            start_time = start_time
        )

        return reservation, (user, table, restaurant, start_time)

    @staticmethod
    def assertEqualReservations(r1, r2):
        t = unittest.FunctionTestCase(TestReservation)
        t.assertEqual(r1.user.id, r2.user.id)
        t.assertEqual(r1.table.id, r2.table.id)
        t.assertEqual(r1.restaurant.id, r2.restaurant.id)
        t.assertEqual(r1.people_number, r2.people_number)
        t.assertEqual(r1.start_time, r2.start_time)

    def test_reservation_init(self):
        reservation, (user, table, restaurant, start_time) = TestReservation.generate_random_reservation()
        self.assertEqual(reservation.user, user)
        self.assertEqual(reservation.table, table)
        self.assertEqual(reservation.start_time, start_time) 
        self.assertEqual(reservation.end_time, start_time+timedelta(hours=reservation.MAX_TIME_RESERVATION))

        
    def test_set_end_time_by_avg_stay(self):
        reservation, _ = TestReservation.generate_random_reservation()
        restaurant = reservation.restaurant
        restaurant.set_avg_stay(240)
        end_time = reservation.start_time + timedelta(hours=4)
        reservation.set_end_time_by_avg_stay(restaurant.avg_stay)
        self.assertEqual(reservation.end_time, end_time)
    # def test_set_start_time(self):
    #     reservation, _ = TestReservation.generate_random_reservation()
    #     wrong_start_time = TestReservation.faker.date_time_between('-4y','now')
    #     with self.assertRaises(ValueError):
    #             reservation.set_start_time(wrong_start_time)

    def test_set_user(self):
        reservation,_= TestReservation.generate_random_reservation()
        user = self.test_user.generate_random_user()
        reservation.set_user(user)
        self.test_user.assertUserEquals(user, reservation.user)

    def test_set_table(self):        
        reservation, _ = TestReservation.generate_random_reservation()
        table, _  = self.test_table.generate_random_table()
        reservation.set_table(table)
        self.test_table.assertEqualTables(table, reservation.table)

    def test_set_restaurant(self):
        reservation, _ = TestReservation.generate_random_reservation()
        restaurant, _  = self.test_restaurant.generate_random_restaurant()
        reservation.set_restaurant(restaurant)
        self.test_restaurant.assertEqualRestaurants(restaurant, reservation.restaurant)


    def test_set_people_number(self):
        reservation, _ = TestReservation.generate_random_reservation()
        people_number = self.faker.random_int(min=0, max=reservation.table.capacity)
        reservation.set_people_number(people_number)
        self.assertEqual(people_number, reservation.people_number)

    def test_check_time(self):
        reservation, _ = TestReservation.generate_random_reservation()
        start_time = self.faker.date_time_between('now', '+14d')
        end_time = self.faker.date_time_between('-3d', 'now')
        with self.assertRaises(ValueError):
            reservation.check_time(start_time, end_time)

    def test_set_end_time(self):
        reservation, _ = TestReservation.generate_random_reservation()
        wrong_endtime = self.faker.date_time_between_dates(
            datetime_start=reservation.start_time - timedelta(days=3), 
            datetime_end=reservation.start_time
            )
        with self.assertRaises(ValueError):
                reservation.set_end_time(wrong_endtime)

    def test_set_is_confirmed(self):
        reservation, _ = TestReservation.generate_random_reservation()
        reservation.set_is_confirmed()
        self.assertTrue(reservation.is_confirmed)