from . import fixtures
from .helpers import GeneralTestCase
from instacommander import renderers
from nose.plugins.attrib import attr
import os

MODULE_PATH = os.path.split(os.path.realpath(__file__))[0]
ARTIFACT_PATH = os.path.join(MODULE_PATH, "artifacts")


class FiltersTestCase(GeneralTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def make_artifact(self, filename, content):
        '''
        Creates an artifact on the filesystem for manual viewing.
        '''
        with open(os.path.join(ARTIFACT_PATH, filename), 'w+') as artifact:
            artifact.write(content)
            artifact.flush()
            artifact.close()

    # @attr('single')
    def test_to_ascii(self):
        'Testing InstaCommander.renderers.to_ascii'
        img_fp = fixtures.typical_picture()

        ascii_stream = renderers.to_ascii(img_fp)
        self.assertGreater(len(ascii_stream), 1, "ASCII successfully converted")

        # Test all the charsets
        for charset in ['ascii', 'shades', 'blocks']:
            ascii_stream = renderers.to_ascii(img_fp, charset=charset)
            self.assertGreater(len(ascii_stream), 1, "ASCII successfully converted")
            self.make_artifact("ascii_charset_{}.txt".format(charset), ascii_stream)
