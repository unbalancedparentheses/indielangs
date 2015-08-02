#!/usr/bin/env python

"""Webserver for indie lanugages"""

import os
import json
import time
import rethinkdb as r
from flask import Response, Flask

DB_HOST = os.getenv('DB', 'localhost')
DB = r.connect(DB_HOST)

app = Flask(__name__)


@app.route("/")
def index():
    """Returns the list of languages available in github
    with the epoch date on which they were added to it"""
    langs_db = languages_db()

    if langs_db:
        languages = langs_db['languages']
        timestamp = int(langs_db['timestamp'].strftime("%s"))
    else:
        languages = []
        timestamp = int(time.time())

    ret = json.dumps({'languages': languages,
                      'timestamp': timestamp})
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp


def languages_db():
    """Get the languages stored in the database"""
    s_langs = (r.db('indielangs')
               .table('languages')
               .order_by(r.desc('timestamp'))
               .limit(1).run(DB))

    if len(s_langs) != 0:
        return s_langs[0]
    else:
        return {}

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
