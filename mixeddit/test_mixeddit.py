import json
from mixeddit.mixeddit import Mixeddit
import unittest


class Test_Mixeddit(unittest.TestCase):

    def test_title_parsing(self):
        with open('testFiles/Reddit/parseRedditTitle.json', 'r') as json_file:
            test_json = json.load(json_file)
            for submission in range(0, len(test_json)):
                with self.subTest(submission=test_json[submission]):
                    rso = Mixeddit(test_json[submission]["ogTitle"])
                    self.assertEqual(rso.reddit_title,
                                     test_json[submission]["ogTitle"])
                    if(test_json[submission]["valid"]):
                        self.assertEqual(rso.artist,
                                         test_json[submission]["artist"])
                        self.assertEqual(rso.track,
                                         test_json[submission]["track"])
                    else:
                        self.assertIsNone(rso.artist)
                        self.assertIsNone(rso.track)

if __name__ == '__main__':
    unittest.main()
