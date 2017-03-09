#!/usr/bin/env python3
'''Local test server'''

import argparse

from app import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch a local test '
                                     'server for Kantinemeny')
    parser.add_argument('-p', '--port', dest='port', type=int, default=5453,
                        help='Specify the port the interface instance should '
                        'listen on. Default: 5453')
    parser.add_argument('-i', '--bind', dest='host', default='0.0.0.0',
                        help='Specify the IP the interface instance should '
                        'listen on. Default: 0.0.0.0')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True, threaded=True)

