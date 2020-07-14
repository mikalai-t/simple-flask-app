#!/usr/bin/env python3

import os
import socket
import pprint
from flask import jsonify, request, Response


def home_page():
    req_dict = request.__dict__

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        req_dict['ip_address'] = s.getsockname()[0]
    except ConnectionError:
        req_dict['ip_address'] = socket.gethostbyname_ex(socket.gethostname())[-1]
    finally:
        s.close()

    req_dict['hostname'] = socket.gethostname()
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

    return 'Hello, <b>{}</b>, from application, running on <u>{}</u>. You visited this node <b>{}</b> time(s).'.format(
        name, socket.gethostname(), counter)
