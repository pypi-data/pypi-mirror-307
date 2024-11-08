import unittest
import random

from clibox import Box

class TestBox(unittest.TestCase):

    @staticmethod
    def run_all():
        for i in range(5):
            unittest.main()

    def testCreation(self):
        box = Box(1,2,False)
        self.assertIsInstance(box, Box)
        self.assertEqual(box._width, 1)
        self.assertEqual(box._height, 2)

    def testSetContent(self):
        w = random.randint(1, 100)
        h = random.randint(1, 100)
        box = Box(w,h, True)
        box.setContent(" "*w*h)

        # Assert height of the content
        self.assertEqual(len(box._content), h)

        # Assert width of the content
        for l in box._content:
            self.assertEqual(len(l), w)
        
