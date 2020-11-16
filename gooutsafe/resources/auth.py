from gooutsafe.dao.user_manager import UserManager


def authenticate(email, password):
    """Allows the user to log into the system

    Args:
        the user's session is new or needs to be reloaded. Defaults to False.

    Returns:
        Returns the response to microservice
    """
    user = UserManager.retrieve_by_email(email)
    if user and user.authenticate(password):
        return None, 200

    return None, 401
