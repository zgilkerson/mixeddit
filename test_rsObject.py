import json
from rsObject import rsObject
import unittest

class TestrsObject(unittest.TestCase):

    def test_titleParsing(self):
        with open('testCases.json', 'r') as testJson:
            loadedJson = json.load(testJson)
            for i in range(0, len(loadedJson)):
                with self.subTest(i=loadedJson[i]):
                    rso = rsObject(loadedJson[i]["ogTitle"])
                    self.assertEqual(rso.ogTitle, loadedJson[i]["ogTitle"])
                    if(loadedJson[i]["valid"]):
                        self.assertEqual(rso.artist, loadedJson[i]["artist"])
                        self.assertEqual(rso.track, loadedJson[i]["track"])
                    else:
                        self.assertIsNone(rso.artist)
                        self.assertIsNone(rso.track)

if __name__ == '__main__':
    unittest.main()
