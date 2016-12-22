from contextlib import contextmanager
import dis
from flask import jsonify, request, url_for
from flask_restful import abort, Api, Resource, reqparse, fields, marshal
import sys
from io import StringIO


@contextmanager
def captureStdOut(output):
    stdout = sys.stdout
    sys.stdout = output
    yield
    sys.stdout = stdout


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
        parser = reqparse.RequestParser()
        parser.add_argument('payload', type=str, help='Payload as code, to be analyzed by Unravelr.')
        args = parser.parse_args()

        try:
            Binary = compile(args['payload'], "<string>", "exec")
            result = StringIO()
            with captureStdOut(result):
                dis.dis(Binary)
            # import ipdb; ipdb.set_trace()
            return jsonify(dict(result=result.getvalue()))
        except:
            abort(404)
