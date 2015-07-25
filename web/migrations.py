#!/usr/bin/env python

"""Migrations for languages model"""

import os
import rethinkdb as r
import sys

DB_HOST = os.getenv('DB', 'localhost')
DB = r.connect(DB_HOST)


def main():
    """Setup database"""
    r.db_create('indielangs').run(DB)
    r.db('indielangs').table_create('languages').run(DB)

if __name__ == "__main__":
    sys.exit(main())
