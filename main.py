#!/usr/bin/env python3

import os
from flask import Flask
from ext import views
from werkzeug.utils import import_string


app = Flask(__name__)

app.config.from_object(import_string('config.{}Config'.format(os.environ['FLASK_ENV'].capitalize()
                                                              if 'FLASK_ENV' in os.environ else ''))())

app.add_url_rule("/", view_func=views.home_page)
app.add_url_rule("/health", view_func=views.health_check)
app.add_url_rule("/hello/<name>", view_func=views.hello)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
