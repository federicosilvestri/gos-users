import unittest


class DaoTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests models
    """

    @classmethod
    def setUpClass(cls):
        from gooutsafe import create_app
        create_app()
