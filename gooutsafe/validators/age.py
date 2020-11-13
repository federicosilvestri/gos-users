import datetime
from wtforms.validators import ValidationError


class AgeValidator(Exception):
    def __init__(self, min_age=0, max_age=0):
        """
        Age validation
        :param min_age: 0 means no limit
        :param max_age: 0 means no limit
        """
        self.min_age = min_age
        self.max_age = max_age

        if type(min_age) != int and type(min_age) != int:
            raise ValueError('min_age and max_age must be integers!')

        if min_age < 0 or max_age < 0:
            raise ValueError('min_age(%d) and max_age(%d) must be positive!' % (min_age, max_age))

        if min_age > max_age != 0:
            raise ValueError('max_age(%d) must be greater than min_age(%d)!' % (max_age, min_age))

        self.message = ""

    def __call__(self, form, field):
        check_year = field.data

        if check_year:
            current_year = datetime.date.today()
            difference = current_year - check_year
            years = difference.days / 365.25

            if self.max_age == 0:
                # means no upper bound
                if years < self.min_age:
                    valid = False
                    self.message = "You are too young!"
                else:
                    valid = True
            elif self.min_age == 0:
                if years > self.max_age:
                    valid = False
                    self.message = "You are too old!"
                else:
                    valid = True
            else:
                # bounds
                if years > self.max_age:
                    valid = False
                    self.message = "You are too old!"
                elif years < self.min_age:
                    valid = False
                    self.message = "You are too young!"
                else:
                    valid = True
        else:
            self.message = "Invalid date"
            valid = False

        if not valid:
            raise ValidationError(self.message)
