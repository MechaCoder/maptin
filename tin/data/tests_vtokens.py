from unittest import TestCase
from random import randint, choice
from os import remove, listdir

from tinydb.database import Document
from faker import Faker

from .vTokens import vTokenData


class testvTokenData(TestCase):

    def setUp(self):
        self.testFile = 'unitTest.ds.json'
        self.db = vTokenData(file=self.testFile)
        if self.db.readAll() == []:

            for e in range(0, 20):
                self.db.create(
                    mapHex='testMap',
                    source='/static/tea_break_by_mattdixon_dd1un2s.jpg',
                    tokenType='token',
                    x=randint(0, 5000),
                    y=randint(0, 5000),
                )

        return super().setUp()


    def test_create(self):

        obj = self.db.create(
            mapHex='testMap',
            source='/static/tea_break_by_mattdixon_dd1un2s.jpg',
            tokenType='token',
            x=randint(0, 5000),
            y=randint(0, 5000),
        )

        self.assertIsInstance(
            obj,
            int
        )

    def test_readByMapHex(self):

        rows = self.db.readByMapHex('testMap')
        for row in rows:

            self.assertIsInstance(
                row,
                Document
            )

    def test_updateByHex(self):

        randDoc = choice(seq=self.db.readAll())

        obj = self.db.updateByHex(
            randDoc['hex'],
            randint(0, 5000),
            randint(0, 5000)
        )

        self.assertIsInstance(obj, list)

        for row in obj:
            self.assertIsInstance(row, int)

    def test_deleteByHex(self):

        randDoc = choice(seq=self.db.readAll())
        self.db.deleteByHex(randDoc['hex'])
        doc = self.db.readById(randDoc.doc_id)

        self.assertIsNone(
            doc
        )

    def test_getPopluarty(self):

        prop = self.db.getPopluarty()
        self.assertIsInstance(
            prop,
            list
        )

        for img in prop:
            self.assertIsInstance(img, str)
