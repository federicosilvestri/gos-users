import datetime
from datetime import time

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, TimeField


class FilterForm(FlaskForm):
    """Form created to allow the operator to filter his reservation, 
    for the restaurant
    """

    filter_date = DateField(default=datetime.date.today())
    start_time = TimeField(default=time(hour=0))
    end_time = TimeField(default=time(hour=23))

    display = ['filter_date', 'start_time', 'end_time']
