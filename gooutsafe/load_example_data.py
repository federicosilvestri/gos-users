import json

PATH_HEALTH_AUTH_DATA = './gooutsafe/example_data/health_authority.json'


def load_health_auth_data():
    with open(PATH_HEALTH_AUTH_DATA) as json_file:
        dict_health_auth = json.load(json_file)

    email = dict_health_auth["email"]
    password = dict_health_auth["password"]
    name = dict_health_auth["name"]
    city = dict_health_auth["city"]
    address = dict_health_auth["address"]
    phone = dict_health_auth["phone"]

    from gooutsafe.models import health_authority
    lha = health_authority.Authority(email=email, name=name,
                                     city=city,
                                     address=address, phone=phone
                                     )
    lha.set_password(password)

    from gooutsafe.dao.health_authority_manager import AuthorityManager
    AuthorityManager.create_authority(lha)


def load_random_customer(n: int):
    from gooutsafe.dao.customer_manager import CustomerManager
    from tests.models.test_customer import TestCustomer

    for _ in range(0, n):
        customer, _ = TestCustomer.generate_random_customer()
        CustomerManager.create_customer(customer=customer)

    print('Random users added to db')


if __name__ == "__main__":
    import sys
    import gooutsafe

    gooutsafe.create_app()

    if len(sys.argv) == 1:
        load_health_auth_data()
    elif len(sys.argv) > 2 and sys.argv[1] == 'users':
        load_random_customer(int(sys.argv[2]))
