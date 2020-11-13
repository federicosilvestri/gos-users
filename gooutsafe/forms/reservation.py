import datetime
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class ReservationForm(FlaskForm):
    """Form created to allow the customers to book a table in a restaurant,
    specifying the date, the time and the number of people
    """

    start_date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Time', format='%H:%M',validators=[DataRequired()])
    people_number = IntegerField('Number of Persons',
                                 validators=[
                                     NumberRange(min=1, max=20),
                                     DataRequired()
                                 ]
                                 )

    def validate_on_submit(self):
        date = self.start_date.data
        time = self.start_time.data
        people_number = self.people_number.data
        print(time)
        start_time_merged = datetime.combine(date, time)
        if start_time_merged < datetime.now() or people_number <= 0:
            return False
        else:
            return True

    display = ['start_date', 'start_time', 'people_number']
