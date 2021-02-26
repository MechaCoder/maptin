from unittest import TestCase

import tin.commons as commons

class TestCommons(TestCase):

    def testSuccess(self):

        obj = commons.success()

        self.assertIsInstance(
            obj,
            dict
        )

        self.assertIn(
            'succ',
            obj.keys()
        )

        self.assertTrue(
            obj['succ'],
        )

        self.assertIn(
            'data',
            obj.keys()
        )

        self.assertIsInstance(
            obj['data'],
            dict
        )

    def testFail(self):
        
        obj = commons.fail()

        self.assertIsInstance(
            obj,
            dict
        )

        self.assertIn(
            'succ',
            obj.keys()
        )

        self.assertFalse(
            obj['succ'],
        )

        self.assertIn(
            'err',
            obj.keys()
        )

        self.assertIsInstance(
            obj['err'],
            str
        )


