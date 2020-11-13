import wtforms as f
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired


class UpdateCustomerForm(FlaskForm):
    """Form created to allow the customers modify their personal information
    """

    email = EmailField(
        'email',
        validators=[DataRequired()]
    )

    password = f.PasswordField(
        'password',
        validators=[DataRequired()]
    )

    phone = TelField(
        'phone',
        validators=[DataRequired()]
    )

    display = ['email', 'password', 'phone']
    

class AddSocialNumberForm(FlaskForm):
    """Form created to allow the customers insert, even after the sign up,
    their personal Social Security Number
    """

    social_number = f.StringField(
        'Social Number',
        validators=[DataRequired()]
    )

    display = ['social_number']
