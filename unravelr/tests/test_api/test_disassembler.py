from ..mixins import TestCaseMixin
from nose.plugins.attrib import attr
import json


class DisassemblerTestCase(TestCaseMixin):

    # @attr('single')
    def test_get(self):
        "Testing api.Disassembler.get"
        r = self.client.get("/api/disassembler")
        self.assertEquals(r.status_code, 200)
        # self.assertGreaterEqual(len(r.json['ciphers']), 2, "Payload serializable.")

    # @attr('single')
    def test_post(self):
        "Testing api.Disassembler.post on valid input"
        r = self.client.post(
            "/api/disassembler",
            data=json.dumps({"payload": """x=abs(-9)"""}),
            content_type='application/json',)
        self.assertEquals(r.status_code, 200)
        self.assertGreaterEqual(len(r.json), 1, "Payload serializable.")
