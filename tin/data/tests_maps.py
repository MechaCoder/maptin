from typing import Container
from unittest import TestCase
from random import randint, choice

from tinydb.database import Document
from faker import Faker

from .maps import Maps

class TestMaps(TestCase):

    def setUp(self) -> None:
        testFile = 'unitTest.ds.json'
        self.db = Maps(file=testFile)
        return super().setUp()
    
    def test_create(self):
        
        obj = self.db.create(
            owner_id=randint(0, 10),
            title=Faker().name(),
            mapsource='static/world-map.gif',
            soundtrack=Faker().url(),
            width=randint(0, 5000),
        )

        self.assertIsInstance(obj, int)

    def test_readByOwnerId(self):
        
        if len(self.db.readAll()) < 100:
            for x in range(1, 100):
                self.db.create(
                    owner_id=randint(0, 10),
                    title=Faker().name(),
                    mapsource='static/world-map.gif',
                    soundtrack=Faker().url(),
                    width=randint(0, 5000),
                )

        keys = ['hex', 'owner_id',  'title', 'map_source', 'map_soundtrack', 'width', 'fog']

        for row in self.db.readByOwnerId(randint(0, 10)):
            self.assertIsInstance(
                row,
                Document
            )

            for k in keys:
                self.assertIn(
                    member=k,
                    container=row.keys()
                )
            pass
        pass

    def test_readByHex(self):

        randDoc = choice(seq=self.db.readAll())

        testObj = self.db.readByHex(hex=randDoc['hex'])

        self.assertEqual(
            first=randDoc,
            second=testObj
        )
        

