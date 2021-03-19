from unittest import TestCase
from random import choice, randint
from faker import Faker

from maptin.data.commons import Document
from maptin.data.maps import Map
from maptin.data.users import User

class TestMap(TestCase):

    def setUp(self):
        self.testObject = Map(True)
        return super().setUp()

    def test_create(self):

        users = User().getAll()
        if users == []:
            User().create(
                email=Faker().email(),
                password=Faker().unique.name(),
                commonName=Faker().name()
            )
            users = User().getAll()

        doc = choice(users)
        
        obj = self.testObject.create(
            doc['id'],
            '/static/world-map.gif',
            'https://www.youtube.com/watch?v=_3r-A7hbbMw'
        )

        self.assertIsInstance(
            obj,
            str
        )


    def test_readAll(self):

        obj = self.testObject.readAll()
        self.assertIsInstance(obj, list)
        
        for row in obj:
            self.assertIsInstance(
                row,
                Document
            )

            self.assertIn(
                'hex',
                row.keys()
            )

            self.assertIn(
                'title',
                row.keys()
            )

            self.assertIn(
                'owner_id',
                row.keys()
            )

            self.assertIn(
                'map_background',
                row.keys()
            )

            self.assertIn(
                'map_soundtrack',
                row.keys()
            )

            self.assertIn(
                'map_width',
                row.keys()
            )

            self.assertIn(
                'map_fog',
                row.keys()
            )

    def test_readByHex(self):

        users = User().getAll()
        if users == []:
            User().create(
                email=Faker().email(),
                password=Faker().unique.name(),
                commonName=Faker().name()
            )
            users = User().getAll()

        doc = choice(users)

        hex = self.testObject.create(#  create a new hex.
            doc['id'],
            '/static/world-map.gif',
            'https://www.youtube.com/watch?v=_3r-A7hbbMw'
        )

        rows = self.testObject.readByHex(hex)
        self.assertIsInstance(
            rows,
            list
        )

        self.assertEqual(
            len(rows),
            1
        )

        for row in rows:
            self.assertIsInstance(
                row,
                Document
            )

            self.assertIn(
                'hex',
                row.keys()
            )

            self.assertIn(
                'title',
                row.keys()
            )

            self.assertIn(
                'owner_id',
                row.keys()
            )

            self.assertIn(
                'map_background',
                row.keys()
            )

            self.assertIn(
                'map_soundtrack',
                row.keys()
            )

            self.assertIn(
                'map_width',
                row.keys()
            )

            self.assertIn(
                'map_fog',
                row.keys()
            )

    def test_readByOwnerId(self):
        
        f_email = Faker().email()
        User().create(
            f_email,
            Faker().name()
        )

        usr = User().getUserByEmail(f_email)

        x_int = randint(10, 40)
        hexs = []
        while len(hexs) < x_int:
            h = self.testObject.create(
                usr[0]['id'],
                '/static/world-map.gif',
                'https://www.youtube.com/watch?v=_3r-A7hbbMw'
            )
            hexs.append(h)

        rows = self.testObject.readByOwnerId(usr[0]['id'])
        self.assertEqual(
            len(rows),
            x_int
        )

    def test_updateByHex(self):
        h = self.testObject.create(
            1,
            '/static/world-map.gif',
            'https://www.youtube.com/watch?v=_3r-A7hbbMw'
        )

        self.assertTrue(
            self.testObject.updateByHex(
                h,
                Faker().name(),
                '/static/world-map.gif',
                'https://www.youtube.com/watch?v=_3r-A7hbbMw',
                90000,
                True
            )
        )

    def test_deleteByHex(self):

        h = self.testObject.create(
            1,
            '/static/world-map.gif',
            'https://www.youtube.com/watch?v=_3r-A7hbbMw'
        )

        obj = self.testObject.deleteByHex(h)
        self.assertTrue(obj)



