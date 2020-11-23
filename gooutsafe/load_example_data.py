import json

from werkzeug.security import generate_password_hash

PATH_HEALTH_AUTH_DATA = './gooutsafe/example_data/health_authority.json'


def load_health_auth_data():
    with open(PATH_HEALTH_AUTH_DATA) as json_file:
        dict_health_auth = json.load(json_file)

    email = dict_health_auth["email"]
    password = generate_password_hash(dict_health_auth["password"])
    name = dict_health_auth["name"]
    city = dict_health_auth["city"]
    address = dict_health_auth["address"]
    phone = dict_health_auth["phone"]

    from gooutsafe.models import health_authority
    lha = health_authority.Authority(email=email, password=password, name=name,
                                     city=city,
                                     address=address, phone=phone
                                     )

    from gooutsafe.dao.health_authority_manager import AuthorityManager
    AuthorityManager.create_authority(lha)
