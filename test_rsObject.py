import json
import rsObject
import unittest

class TestrsObject(unittest.TestCase):

    def test_isParsable(self):
        with open('testCases.json', 'r') as testJson:
            loadedJson = json.load(testJson)
            for i in range(0, len(loadedJson)):
                with self.subTest(i=i):
                    print(str(loadedJson[i])[0])
                    self.assertEqual(str(loadedJson[i])[0], '{')
                # print(loadedJson[i])

if __name__ == '__main__':
    unittest.main()
