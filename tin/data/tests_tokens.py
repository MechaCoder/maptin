from unittest import TestCase
from random import randint, choice
from os import remove

from tinydb.database import Document
from faker import Faker

from .tokens import Tokens


class testTokens(TestCase):

    def setUp(self):
        self.testFile = 'unitTest.ds.json'
        self.db = Tokens(file=self.testFile)
        return super().setUp()

    def test_addKey(self):

        testObj = self.db.addKey(Faker().ascii_email())

        self.assertIsInstance(
            testObj,
            str
        )

        self.assertEqual(
            len(testObj),
            128
        )

    def test_keyExsists(self):

        key = self.db.addKey(Faker().ascii_email())
        testObj = self.db.keyExsists(key)
        self.assertIsInstance(testObj, bool)
        self.assertTrue(testObj)

    def test_getRowByKey(self):

        key = self.db.addKey(Faker().ascii_email())
        obj = self.db.getRowByKey(key=key)

        self.assertIsInstance(
            obj,
            Document
        )
