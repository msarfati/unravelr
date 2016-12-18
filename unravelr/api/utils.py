from io import StringIO
from flask import send_file
from flask.ext.restful import abort, Api, Resource, reqparse, fields, marshal


class SaveToFile(Resource):
    """
    Implements endpoint and functionality of saving to a file.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, help='Raw string to be turned into a file.')
        args = parser.parse_args()

        sio = StringIO(args['message'])
        return send_file(sio.getvalue(), mimetype="text/plain", )
