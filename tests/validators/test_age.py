import datetime
import random

from faker import Faker
from wtforms.validators import ValidationError

from .validator_test import ValidatorTest


class AnonymousField:
    def __init__(self, data):
        self.data = data


class TestAgeValidator(ValidatorTest):
    faker = Faker()

    def setUp(self):
        super(TestAgeValidator, self).setUp()
        from gooutsafe.validators import age

        self.age_validator = age

    def test_init_str(self):
        with self.assertRaises(ValueError):
            self.age_validator.AgeValidator(min_age=TestAgeValidator.faker.street_name())
            self.age_validator.AgeValidator(max_age=TestAgeValidator.faker.street_name())
            self.age_validator.AgeValidator(
                min_age=TestAgeValidator.faker.street_name(),
                max_age=TestAgeValidator.faker.street_name()
            )

    def test_init_bounds(self):
        with self.assertRaises(ValueError):
            self.age_validator.AgeValidator(min_age=-1)
            self.age_validator.AgeValidator(max_age=-1)
            self.age_validator.AgeValidator(min_age=-1, max_age=-1)

    def test_init_validity(self):
        with self.assertRaises(ValueError):
            self.age_validator.AgeValidator(
                min_age=random.randint(101, 200),
                max_age=random.randint(0, 100)
            )

        self.age_validator.AgeValidator(
            min_age=random.randint(0, 100),
            max_age=random.randint(101, 200)
        )

    def test_invalid_date(self):
        av = self.age_validator.AgeValidator(
            min_age=0,
            max_age=30
        )

        with self.assertRaises(ValidationError):
            av.__call__(None, AnonymousField(None))

    def test_valid_call_unbounded(self):
        av = self.age_validator.AgeValidator(
            min_age=0,
            max_age=30
        )

        valid_date = datetime.date.today()
        field = AnonymousField(valid_date)

        av.__call__(None, field)

        av = self.age_validator.AgeValidator(
            min_age=30,
            max_age=0
        )

        valid_date = datetime.date.today() - datetime.timedelta(days=365.25 * 40)
        field = AnonymousField(valid_date)

        av.__call__(None, field)

    def test_valid_call_bounded(self):
        av = self.age_validator.AgeValidator(
            min_age=10,
            max_age=30
        )

        valid_date = datetime.date.today() - datetime.timedelta(days=365.5 * 20)
        field = AnonymousField(valid_date)

        av.__call__(None, field)

    def test_invalid_call_bounded(self):
        av = self.age_validator.AgeValidator(
            min_age=10,
            max_age=30
        )

        invalid_date = datetime.date.today()
        field = AnonymousField(invalid_date)

        with self.assertRaises(ValidationError):
            av.__call__(None, field)

        av = self.age_validator.AgeValidator(
            min_age=10,
            max_age=30
        )

        invalid_date = datetime.date.today() - datetime.timedelta(days=365.25 * 40)
        field = AnonymousField(invalid_date)

        with self.assertRaises(ValidationError):
            av.__call__(None, field)

    def test_invalid_call_unbounded(self):
        av = self.age_validator.AgeValidator(
            min_age=0,
            max_age=30
        )

        valid_date = datetime.date.today() - datetime.timedelta(days=365.5 * 40)
        field = AnonymousField(valid_date)

        with self.assertRaises(ValidationError):
            av.__call__(None, field)

        av = self.age_validator.AgeValidator(
            min_age=30,
            max_age=0
        )

        valid_date = datetime.date.today() - datetime.timedelta(days=365.5 * 20)
        field = AnonymousField(valid_date)

        with self.assertRaises(ValidationError):
            av.__call__(None, field)
