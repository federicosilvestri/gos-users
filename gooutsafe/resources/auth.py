from gooutsafe.dao.user_manager import UserManager


def authenticate(auth):
    """
    Authentication resource for generic user.
    :param auth: a dict with email and password keys.
    :return: the response 200 if credentials are correct, else 401
    """
    user = UserManager.retrieve_by_email(auth['email'])
    if user and user.authenticate(auth['password']):
        return None, 200

    return None, 401
