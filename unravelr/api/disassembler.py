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
            return jsonify(message="POST your code into the 'payload' field to be analyzed by Unravelr.")
        except:
            abort(404)

    def post(self):

        # import ipdb; ipdb.set_trace()
        parser = reqparse.RequestParser()
        parser.add_argument('payload', type=str, help='Payload as code, to be analyzed by Unravelr.')
        args = parser.parse_args()

        try:
            import dis
            Binary = compile(args['payload'], "<string>", "exec")
            result = dis.dis(Binary)
            # import ipdb; ipdb.set_trace()
            return jsonify(dict(result=result))
        except:
            abort(404)
