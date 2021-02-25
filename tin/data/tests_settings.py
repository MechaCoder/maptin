from unittest import TestCase
from random import randint, choice
from os import remove

from tinydb.database import Document
from faker import Faker

from .settings import Settings

class TestSettings(TestCase):

    def setUp(self):
        self.testFile = 'unitTest.ds.json'
        self.db = Settings(file=self.testFile)
        return super().setUp()

    def test_resetSessionSysKey(self):

        oldKey = self.db.get('sessionSysKey')
        self.db.resetSessionSysKey()
        newKey = self.db.get('sessionSysKey')

        self.assertNotEqual(
            oldKey,
            newKey
        )