#!/usr/bin/env python
"""
Fetch github linguist repository, process its information
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
    Execute run at the beggining and every hour.
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
    """
    Obtain the languages names and their respective metadata
    to store in the database.
    """
    langs = gitlog.languages()
    db.store(langs)


if __name__ == "__main__":
    sys.exit(main())
