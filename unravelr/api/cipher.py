from .. import cipher as cipher_alg
from flask import jsonify, request, url_for
from flask.ext.restful import abort, Api, Resource, reqparse, fields, marshal

cipher_alg_lookup = {
    "rc4": {
        "_algorithm": cipher_alg.RC4,
        "name": "rc4",
        "other_names": ['Rivest Cipher 4', 'ARC4', 'ARCFOUR'],
        "wiki": "https://en.wikipedia.org/wiki/RC4",
    },
    "tea": {
        "_algorithm": None,
        "name": "tea",
        "other_names": ['Tiny Encryption Algorithm'],
        "wiki": "https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm",
    }
}


def cipher_alg_lookup_validator(cipher):
    try:
        return cipher_alg_lookup[cipher]
    except:
        return abort(404, message="Cipher '{}' is invalid. Please get the current list of ciphers".format(cipher))


class Ciphers(Resource):
    """
    Operations dealing with all ciphers
    """
    # decorators = [auth.login_required]

    def get(self):
        """
        Returns a list of currently supported ciphers.
        """
        try:
            return jsonify(ciphers=list(cipher_alg_lookup.keys()))
        except:
            abort(404)

    def post(self):
        pass


class Cipher(Resource):
    """
    Operations dealing with individual ciphers
    """
    # decorators = [auth.login_required]

    def get(self, cipher):
        # import ipdb; ipdb.set_trace()
        cipher = cipher_alg_lookup_validator(cipher)

        try:
            # import ipdb; ipdb.set_trace()
            return jsonify(**{k: v for k, v in cipher.items() if k[0] is not "_"})
        except:
            abort(404)


class CipherEncrypt(Resource):
    """
    Handles looking up the cipher, and encrypting the plaintext.
    """
    def post(self, cipher):
        cipher = cipher_alg_lookup_validator(cipher)

        # import ipdb; ipdb.set_trace()
        parser = reqparse.RequestParser()
        parser.add_argument('key', type=str, help='Secret key, used to encrypt your message.')
        parser.add_argument('message', type=str, help='The plaintext that will be encrypted')
        args = parser.parse_args()

        cipher_alg = cipher['_algorithm']
        cipher_alg = cipher_alg(key=args['key'])
        try:
            # import ipdb; ipdb.set_trace()
            return jsonify(dict(
                ciphertext=cipher_alg.encrypt(plaintext=args['message']),
                key=args['key'],
                plaintext=args['message'],
                cipher=cipher['name']))
        except:
            abort(404)


class CipherDecrypt(Resource):
    """
    Handles looking up the cipher, and decryptnig the ciphertext.
    """
    def post(self, cipher):
        cipher = cipher_alg_lookup_validator(cipher)

        # import ipdb; ipdb.set_trace()
        parser = reqparse.RequestParser()
        parser.add_argument('key', type=str, help='Secret key, used to encrypt your message.')
        parser.add_argument('message', type=str, help='The ciphertext that will be decrypted')
        args = parser.parse_args()

        cipher_alg = cipher['_algorithm']
        cipher_alg = cipher_alg(key=args['key'])
        try:
            # import ipdb; ipdb.set_trace()
            return jsonify(dict(
                ciphertext=args['message'],
                key=args['key'],
                plaintext=cipher_alg.decrypt(ciphertext=args['message']),
                cipher=cipher['name']))
        except:
            abort(404)
