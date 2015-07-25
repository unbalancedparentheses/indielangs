#!/usr/bin/env python

"""
Fetches github linguist repository, process its information
and store it in database
"""

import os
import rethinkdb as r
import schedule
import shutil
import subprocess
import sys
import time
import yaml

DEVNULL = open(os.devnull, 'wb')

LANGUAGES_REPO = "https://github.com/github/linguist.git"
LANGUAGES_PATH = "./lib/linguist/languages.yml"
SLEEP_MINUTES = 10

DB_HOST = os.getenv('DB', 'localhost')
DB = r.connect(DB_HOST, 28015)


def main():
    """
    xecutes the job at the beggining and at every SLEEP_MINUTES
    """
    job()
    schedule.every(SLEEP_MINUTES).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


def job():
    """
    Returns the list of languages available in the language file
    with the date in which it was added
    """
    language_history = set()
    result = {}

    prepare()

    for i, commit in enumerate(commits()):
        actual = languages_in_commit(commit)

        if i == 0:
            timestamp = commit_time(commit)

            for language in actual:
                result[language] = timestamp

            language_history = language_history.union(set(actual))

        else:
            old = language_history
            language_history = language_history.union(set(actual))
            diff = language_history - old

            if diff:
                timestamp = commit_time(commit)

                for language in diff:
                    result[language] = timestamp

    filtered = filter_deleted(result)
    store(filtered)
    clean()


def prepare():
    """
    Clone the linguist repo and change the working directory to it.
    It also deletes the linguist directory it if was already present
    """
    if os.path.exists(LANGUAGES_PATH):
        shutil.rmtree("linguist")

    subprocess.call(["git", "clone", LANGUAGES_REPO],
                    stdout=DEVNULL, stderr=DEVNULL)
    os.chdir("linguist")


def clean():
    """
    Return to the previous working directory and remove the linguist directory
    """
    os.chdir("..")
    shutil.rmtree("linguist")


def commits():
    """
    Returns the list of commits in ascending order that changed
    the languages file without counting the commit merges
    """
    commits_b = subprocess.check_output(["git", "log", "--no-merges",
                                         "--pretty=%H", LANGUAGES_PATH],
                                        stderr=DEVNULL)
    commits_reverse = commits_b.decode().strip().split('\n')

    return commits_reverse[::-1]


def languages_lang_file():
    """
    Returns the list of languages present in the language file
    """
    with open(LANGUAGES_PATH) as langs_file:
        try:
            languages_yaml = yaml.load(langs_file)
            return list(languages_yaml.keys())
        except:
            return []


def languages_in_commit(commit):
    """
    Returns the list of languages
    present in the language file for a specific commit
    """
    subprocess.call(["git", "checkout", commit, LANGUAGES_PATH],
                    stdout=DEVNULL, stderr=DEVNULL)
    return languages_lang_file()


def commit_time(commit):
    """
    Returns the commit time in epoc format of a specific commit
    """
    output_b = subprocess.check_output(["git", "show", "-s", "--format=%ct",
                                        commit])
    output = output_b.decode().strip()
    return int(output)


def filter_deleted(languages):
    """
    Returns a hash with the languages that are in the languages argument
    minus the ones that are no longer present in the last commit
    """
    subprocess.call(["git", "reset", "--hard", "master"],
                    stdout=DEVNULL, stderr=DEVNULL)
    last_languages = languages_lang_file()

    filtered_languages = {}

    for lang in languages:
        if lang in last_languages:
            filtered_languages[lang] = languages[lang]

    return filtered_languages


def store(result):
    """
    Stores in database the result.
    If the result is equal to the latest row in the db
    it only updates the timestamp
    """
    serialized = []

    for language in result.keys():
        serialized.append({"name": language, "time": result[language]})

    serialized_order = sorted(serialized, key=lambda lang: lang["time"], reverse=True)

    table = r.db('indielangs').table("languages")
    latest, latest_id = latest_result()

    if latest == serialized_order:
        table.get(latest_id).update({'timestamp': r.now()}).run(DB)
    else:
        row = {'languages': serialized_order, 'timestamp': r.now()}
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


if __name__ == "__main__":
    sys.exit(main())
