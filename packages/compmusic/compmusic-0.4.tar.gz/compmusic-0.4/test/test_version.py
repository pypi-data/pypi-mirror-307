import unittest

import compmusic.version

class VersionTestCase(unittest.TestCase):

    def test_parse_git_describe(self):
        version = '75d4121'
        parsed = compmusic.version.parse_git_describe(version)
        self.assertEqual(parsed, '75d4121')

        version = '75d4121-dirty'
        parsed = compmusic.version.parse_git_describe(version)
        self.assertEqual(parsed, '75d4121')

        version = 'v1.2-g75d4121-dirty'
        parsed = compmusic.version.parse_git_describe(version)
        self.assertEqual(parsed, '75d4121')

        version = 'some-ta-g-14-g75d4121-dirty'
        parsed = compmusic.version.parse_git_describe(version)
        self.assertEqual(parsed, '75d4121')
