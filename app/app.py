#!/usr/bin/env python3

import time

from flask import Flask, render_template, abort, jsonify, request

from kantinemeny import Kantinemeny

app = Flask(__name__)


# Cache menus, by default they are cached for 300 seconds
MENU_VALID_TIME = 300
menus = {}

class Stats(object):
    startup = time.time()
    visits = {
        "api": 0,
        "page": 0
    }





def get_menu(location):
    timestamp = time.time()

    if not menus.get(location, None) or (timestamp - menus[location].timestamp >= MENU_VALID_TIME):
        try:
            menus[location] = Kantinemeny(location)
        except:
            if not menus.get(location, None):
                raise

    return menus[location]


@app.route('/', defaults={'location': 'nostegaten58'})
@app.route('/api/', defaults={'location': 'nostegaten58',
                              'json_response': True})
@app.route('/<location>/')
@app.route('/api/<location>/', defaults={'json_response': True})
def index(location, json_response=False):
    menu = get_menu(location)
    menu_age = time.time() - menu.timestamp

    if json_response:
        return jsonify({'supper': menu.soups,
                        'varmmat': menu.hot_dishes,
                        'dager': menu.days,
                        'meny_sist_sjekket_siden_i_sekunder': menu_age,
                        'meny': menu.filename})

    return render_template('index.html',
                           location=location,
                           menu=menu,
                           start=Stats.startup,
                           fetched='{0:.2f}'.format(menu_age))


if __name__ == "__main__":
    pass
