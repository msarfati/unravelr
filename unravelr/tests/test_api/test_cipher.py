from ..mixins import TestCaseMixin
from nose.plugins.attrib import attr
import json


class CiphersTestCase(TestCaseMixin):

    # @attr('single')
    def test_get(self):
        "Testing api.Ciphers.get"
        r = self.client.get("/api/ciphers")
        self.assertEquals(r.status_code, 200)
        self.assertGreaterEqual(len(r.json['ciphers']), 2, "Payload serializable.")


class CipherTestCase(TestCaseMixin):

    # @attr('single')
    def test_get(self):
        "Testing api.Cipher.get on valid input"
        r = self.client.get("/api/ciphers")
        r = self.client.get("/api/ciphers/" + r.json['ciphers'][0])
        self.assertEquals(r.status_code, 200)
        self.assertGreaterEqual(len(r.json), 3, "Payload serializable.")


class CipherEncryptTestCase(TestCaseMixin):

    # @attr('single')
    def test_post(self):
        "Testing api.Cipher.encrypt on valid input"
        r = self.client.post(
            "/api/ciphers/rc4/encrypt",
            data=json.dumps({"key": "cypher-cossack", "message": "Hello World"}),
            content_type='application/json',)
        self.assertEquals(r.status_code, 200)
        self.assertGreaterEqual(len(r.json), 1, "Payload serializable.")


class CipherDecryptTestCase(TestCaseMixin):

    # @attr('single')
    def test_post(self):
        "Testing api.Cipher.decrypt on valid input"
        r = self.client.post(
            "/api/ciphers/rc4/decrypt",
            data=json.dumps({"key": "cypher-cossack", "message": "7ec387ec9aca52b98f08ca"}),
            content_type='application/json',)
        self.assertEquals(r.status_code, 200)
        self.assertGreaterEqual(len(r.json), 1, "Payload serializable.")
