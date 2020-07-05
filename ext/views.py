#!/usr/bin/env python3

import socket
import pprint
from flask import jsonify, request, Response


def home_page():
    req_dict = request.__dict__
    req_json = pprint.PrettyPrinter().pformat(req_dict)
    return Response(req_json, mimetype='application/json'), 200


def health_check():
    return jsonify({'status': 'up'}), 200


def hello(name):
    return 'Hello, <b>{}</b>, from application, running on <u>{}</u>'.format(name, socket.gethostname())
