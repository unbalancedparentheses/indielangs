"""
Store the languages information in the database
"""
import os
import rethinkdb as r


def store(languages):
    """
    Stores in database the result.
    If the result is equal to the latest row in the db
    it only updates the timestamp
    """
    DB_HOST = os.getenv('DB', 'localhost')
    DB = r.connect(DB_HOST, 28015)

    table = r.db('indielangs').table("languages")
    latest, latest_id = latest_result()

    if latest == languages:
        table.get(latest_id).update({'timestamp': r.now()}).run(DB)
    else:
        row = {'languages': languages, 'timestamp': r.now()}
        table.insert(row).run(DB)


def latest_result():
    """
    Returns the latest row with the list of languages
    available in the database and the id of the row
    """
    table = r.db('indielangs').table("languages")
    latest = table.order_by(r.desc('timestamp')).limit(1).run(DB)

    if latest:
        return latest[0]['languages'], latest[0]['id']
    else:
        return {}, None
