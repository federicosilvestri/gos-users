from gooutsafe.models.customer import Customer
from .manager import Manager
from gooutsafe.comm.manager import EventManager


class CustomerManager(Manager):

    @staticmethod
    def create_customer(customer: Customer):
        Manager.create(customer=customer)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Customer.query.get(id_)
    
    @staticmethod
    def retrieve_by_ssn(ssn):
        Manager.check_none(ssn=ssn)
        return Customer.query.filter_by(social_number=ssn).first()

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email=email)
        return Customer.query.filter_by(email=email).first()
    
    @staticmethod
    def retrieve_by_phone(phone):
        Manager.check_none(phone=phone)
        return Customer.query.filter_by(phone=phone).first()
            
    @staticmethod
    def retrieve_all_positive() -> [Customer]:
        pos_customers = Customer.query.filter_by(health_status=True).all()

        if len(pos_customers) > 0:
            return pos_customers
        return None

    @staticmethod
    def update_customer(customer: Customer):
        Manager.update(customer=customer)

    @staticmethod
    def delete_customer(customer: Customer):
        Manager.delete(customer=customer)
        # trigger the event
        EventManager.customer_deleted(customer.id)

    @staticmethod
    def delete_customer_by_id(id_):
        customer = CustomerManager.retrieve_by_id(id_)
        CustomerManager.delete_customer(customer)
