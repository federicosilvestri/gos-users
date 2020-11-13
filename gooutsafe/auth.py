from flask_login import LoginManager

from gooutsafe.models.user import User


def init_login_manager(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.refresh_view = 'auth.relogin'

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        if user is not None:
            user._authenticated = True
        return user

    return login_manager
