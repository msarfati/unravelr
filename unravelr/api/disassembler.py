from flask import jsonify, request, url_for
from flask_restful import abort, Api, Resource, reqparse, fields, marshal


class Disassembler(Resource):
    """
    Operations dealing with individual ciphers
    """
    # decorators = [auth.login_required]

    def get(self):
        # import ipdb; ipdb.set_trace()

        try:
            # import ipdb; ipdb.set_trace()
            return jsonify(message="Simply POST your payload to be analyzed by Unravelr.")
        except:
            abort(404)

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
