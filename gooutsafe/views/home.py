import json

from flask import Blueprint, render_template, request, flash
from flask_login import current_user

from gooutsafe.dao.restaurant_manager import RestaurantManager
from gooutsafe.forms.restaurant_search import RestaurantSearchForm

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    """General route for the index page
    """
    return render_template("index.html")


@home.route('/search', methods=['GET'])
def search():
    """This method allows customers to search restaurants, using a search bar.
    It's possible to retrieve restaurants based on their name, city or cuisine's type.

    """
    form = RestaurantSearchForm()

    keyword = request.args.get('keyword', default=None, type=str)
    filters = request.args.get('filters', default=None, type=str)

    keyword = None if keyword is None or len(keyword) == 0 else keyword
    json_list = []
    if keyword is not None and filters is None:
        restaurants = search_by(keyword, form.DEFAULT_SEARCH_FILTER)
    elif keyword is not None and filters is not None:
        restaurants = search_by(keyword, filters)
    else:
        restaurants = RestaurantManager.retrieve_all()
        for r in restaurants:
            json_list.append({"name": r.name, "lat": r.lat, "lon": r.lon })
        json_list = json.dumps(json_list)

    return render_template('explore.html', search_form=form, restaurants=restaurants, json_res=json_list)


def search_by(search_field, search_filter):
    """Implements the research of the restaurants

    Args:
        search_field (string)
        search_filter (string)

    """
    if search_filter == "Name":
        restaurants = RestaurantManager.retrieve_by_restaurant_name(search_field)
        return restaurants
    if search_filter == "City":
        restaurants = RestaurantManager.retrieve_by_restaurant_city(search_field)
        return restaurants
    if search_filter == "Menu Type":
        restaurants = RestaurantManager.retrieve_by_menu_type(search_field)
        return restaurants
