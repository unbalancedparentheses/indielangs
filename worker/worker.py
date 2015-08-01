#!/usr/bin/env python
"""
Fetches github linguist repository, process its information
and store it in database
"""
import db
import gitlog
import os
import schedule
import sys
import time

DEVNULL = open(os.devnull, 'wb')


def main():
    """
    Executes the job at the beggining and every hour
    """
    try:
        run()
        schedule.every().hour.do(run)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        gitlog. clean()


def run():
    gitlog.prepare()
    langs = languages()
    db.store(langs)
    gitlog.clean()


def languages():
    dates = gitlog.dates()
    metadata = gitlog.metadata()
    languages = []

    for l in metadata:
        object = {}
        object['name'] = l
        object['timestamp'] = dates[l]

        if metadata[l].get('type', None):
            object['type'] = metadata[l]['type']
        if metadata[l].get('group', None):
            object['group'] = metadata[l]['group']

        languages.append(object)

    sorted_languages = sorted(languages,
                              key = lambda lang: lang["timestamp"],
                              reverse=True)
    return sorted_languages

if __name__ == "__main__":
    sys.exit(main())
