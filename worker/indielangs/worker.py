#!/usr/bin/env python
"""
Fetch github linguist repository, process its information
and store it in database
"""
from indielangs import db
from indielangs import gitlog

import os
import schedule
import sys
import time
import traceback

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
    except Exception as e:
        gitlog.clean()
        print(e)
        traceback.print_exc(file=sys.stdout)
        return 1


def run():
    """
    Obtain the languages names and their respective metadata
    to store in the database.
    """
    langs = gitlog.languages()
    db.store(langs)


if __name__ == "__main__":
    sys.exit(main())
