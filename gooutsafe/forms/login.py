import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Form created to allow users to login
    """

    email = f.StringField(
        'Email',
        validators=[DataRequired()],
        id="inputEmail",
    )
    password = f.PasswordField('Password', validators=[DataRequired()])
    display = ['email', 'password']
