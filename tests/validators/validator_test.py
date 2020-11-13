import unittest


class ValidatorTest(unittest.TestCase):

    def setUp(self):
        from gooutsafe import create_app
        self.app = create_app()
