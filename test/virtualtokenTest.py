from unittest import TestCase
from random import randint
from faker import Faker
from time import time_ns

from maptin.data.commons import Document
from maptin.data.virualtokens import VirtualToken

class TestVirturaltoken(TestCase):

    def test_create(self):

        obj = VirtualToken().create(
            '/static/tea_break_by_mattdixon_dd1un2s.jpg',
            'testMap'
        )

    def test_getByMaphex(self):

        rows = randint(1, 5)
        count = 0

        mapTag = f'testMap_getByMaphex_{time_ns()}'
        while count < rows:
            obj = VirtualToken().create(
                '/static/tea_break_by_mattdixon_dd1un2s.jpg',
                mapTag
            )
            count += 1

        self.assertIsInstance(
            VirtualToken().getByMaphex(mapTag),
            list
        )
        self.assertEqual(
            len(VirtualToken().getByMaphex(mapTag)),
            rows
        )

