from unittest import TestCase
from random import randint, choice
from faker import Faker

from maptin.data.commons import Document
from maptin.data.userKeys import UserTokens

class TestUserkeys(TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_create(self):

        obj = UserTokens().create(9000)
        self.assertIsInstance(
            obj,
            str
        )

        self.assertEqual(
            len(obj),
            256
        )

    def test_getIdByKey(self):
        obj = UserTokens().create(9000)
        uid = UserTokens().removeByKey(obj)

        self.assertIsInstance(uid, int)
        self.assertTrue(uid)

    def test_removeByKey(self):
        obj = UserTokens().create(9000)
        x = UserTokens().removeByKey(obj)

        self.assertTrue(x)