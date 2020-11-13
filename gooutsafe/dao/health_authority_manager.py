from gooutsafe.dao.manager import Manager
from gooutsafe.models.health_authority import Authority


class AuthorityManager(Manager):

    @staticmethod
    def create_authority(authority: Authority):
        Manager.create(authority=authority)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Authority.query.get(id_)
