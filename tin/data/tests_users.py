from unittest import TestCase
from random import randint, choice
from os import remove, uname

from tinydb.database import Document
from faker import Faker

from .users import DataUser


class testDataUser(TestCase):

    def setUp(self):
        self.testFile = 'unitTest.ds.json'
        self.db = DataUser(file=self.testFile)
        self.db.clear()
        return super().setUp()

    def test_makeUser(self):

        uname = Faker().ascii_safe_email()
        pword = Faker().password()

        obj = self.db.makeUser(
            username=uname,
            password=pword
        )

        self.assertIsInstance(
            obj,
            int
        )

    def test_getIdByUname(self):

        uname = Faker().ascii_safe_email()
        pword = Faker().password()

        self.db.makeUser(
            username=uname,
            password=pword
        )

        obj = self.db.getIdByUname(uname=uname)
        self.assertIsInstance(
            obj,
            Document
        )
