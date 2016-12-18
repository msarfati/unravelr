from ..mixins import TestCaseMixin
from nose.plugins.attrib import attr
from cypher_cossack.cipher import RC4


class RC4TestCase(TestCaseMixin):

    # @attr('single')
    def test_encrypt(self):
        "Testing cipher.RC4.encrypt"
        cipher = RC4()
        plaintext = "Hola mundo!"
        ciphertext = cipher.encrypt(plaintext)
        # print(ciphertext); assert False;
        self.assertEquals(len(plaintext), len(ciphertext) / 2, "Ciphertext's length is same as plaintext")

    # @attr('single')
    def test_decrypt(self):
        "Testing cipher.RC4.decrypt"
        cipher = RC4()
        plaintext = "Shit and giggles!"
        ciphertext = cipher.encrypt(plaintext)
        deciphered = cipher.decrypt(ciphertext)
        self.assertEquals(deciphered, plaintext, 'Decryption successful.')

    # @attr('single')
    def test_cs1(self):
        "Ciphersabre example -- still pending"
        cipher = RC4(key="asdfg")
        ciphertext = "6f6d0babf3aa6719031530edb677ca74e0089dd0e7b8854356bb1448e37cdbefe7f3a84f4f5fb3fd"
        cipher.decrypt(ciphertext)
        assert False  # More testing required
