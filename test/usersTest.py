from unittest import TestCase
from random import randint, choice
from faker import Faker

from maptin.data.commons import Document
from maptin.data.users import User

class TestUser(TestCase):

    def setUp(self):
        self.testObject = User()
        return super().setUp()

    def test_create(self):

        obj = self.testObject.create(
            email=Faker().email(),
            password=Faker().unique.name(),
            commonName=Faker().name()
        )

        self.assertTrue(obj)

    def test_vaildate(self):

        email = Faker().email()
        pword = Faker().unique.name()

        self.testObject.create(
            email=email,
            password=pword,
            commonName=Faker().name()
        )

        obj = self.testObject.validate(
            email=email,
            password=pword
        )

        self.assertTrue(obj)