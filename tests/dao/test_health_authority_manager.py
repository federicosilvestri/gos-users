from faker import Faker

from .dao_test import DaoTest


class TestAuthorityManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestAuthorityManager, cls).setUpClass()

        from gooutsafe.dao import health_authority_manager
        cls.health_authority_manager = health_authority_manager.AuthorityManager
        from tests.models.test_authority import TestAuthority
        cls.test_authority = TestAuthority


    def test_crud(self):
        for _ in range(0, 10):
            authority, _ = self.test_authority.generate_random_authority()
            self.health_authority_manager.create_authority(authority=authority)
            authority1 = self.health_authority_manager.retrieve_by_id(authority.id)
            self.test_authority.assertAuthorityEquals(authority1, authority)
