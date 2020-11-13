from .auth import auth
from .home import home
from .restaurants import restaurants
from .users import users
from .reservation import reservation
from .health_authority import authority
from .review import review

"""List of the views to be visible through the project
"""
blueprints = [home, auth, users, restaurants, reservation, authority, review]
