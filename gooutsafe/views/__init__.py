from .auth import auth
from .users import users
from .health_authority import authority

"""List of the views to be visible through the project
"""
blueprints = [auth, users, authority]
