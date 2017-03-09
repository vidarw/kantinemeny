#!/usr/bin/env python3

import os
from flask import send_from_directory

from app.app import app

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')