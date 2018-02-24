import json
from rsObject import rsObject
import unittest

class TestrsObject(unittest.TestCase):

    def test_isParsable(self):
        with open('testCases.json', 'r') as testJson:
            loadedJson = json.load(testJson)
            for i in range(0, len(loadedJson)):
                with self.subTest(i=loadedJson[i]):
                    musicObject = rsObject(loadedJson[i])
                    self.assertEqual(str(musicObject.ogTitle)[0], '{')

if __name__ == '__main__':
    unittest.main()
