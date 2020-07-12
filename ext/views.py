#!/usr/bin/env python3

import os
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
    dest = '/tmp/flask-app/session.counter'
    counter = 0
    if os.path.isdir(os.path.dirname(dest)):
        try:
            with open(dest, 'r') as f:
                counter = int(f.read().strip())
        except (IOError, FileNotFoundError):
            pass
    else:
        try:
            os.makedirs(os.path.dirname(dest), 0o750)
        except (IOError, PermissionError):
            pass

    counter += 1

    try:
        with open(dest, 'w+') as f:
            f.write(str(counter))
    except (IOError, FileNotFoundError, PermissionError):
        pass

    return 'Hello, <b>{}</b>, from application, running on <u>{}</u>. You visited this app <b>{}</b> time(s).'.format(
        name, socket.gethostname(), counter)
