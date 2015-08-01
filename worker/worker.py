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
REPO_DIR = "/tmp/linguist"

DB_HOST = os.getenv('DB', 'localhost')
DB = r.connect(DB_HOST, 28015)


def main():
    """
    Executes the job at the beggining and at every SLEEP_MINUTES
    """
    try:
        run()
        schedule.every().hour.do(run)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        clean()


def run():
    prepare()

    dates = langs_dates()
    metadata = languages_metadata()
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

    store(sorted_languages)

    clean()


def prepare():
    """
    Clone the linguist repo and change the working directory to it.
    It also deletes the linguist directory it if was already present
    """
    clean()
    subprocess.call(["git", "clone", LANGUAGES_REPO, REPO_DIR],
                    stdout=DEVNULL, stderr=DEVNULL)
    os.chdir(REPO_DIR)


def clean():
    """
    Return to the previous working directory and remove the linguist directory
    """
    if os.path.exists(REPO_DIR):
        os.chdir("/")
        shutil.rmtree(REPO_DIR)


def langs_dates():
    """
    Returns the list of languages available in the language file
    with the date in which it was added
    """
    language_history = set()
    result = {}

    for i, commit in enumerate(commits()):
        actual = languages_in_commit(commit)

        if i == 0:
            timestamp = commit_time(commit)

            for language in actual:
                result[language] = timestamp

            language_history = set(actual)
        else:
            old = language_history
            language_history = language_history.union(set(actual))
            diff = language_history - old

            if diff:
                timestamp = commit_time(commit)

                for language in diff:
                    result[language] = timestamp

    filtered = filter_deleted(result)
    return result


def languages_metadata():
    yaml = read_langs_file()
    metadata_keys = ('type', 'group')

    result = {}

    for languages in yaml:
        result[languages] = {k: yaml[languages][k] for k in yaml[languages] if k in metadata_keys}

    return result


def commits():
    """
    Returns the list of commits in ascending order that changed
    the languages file without counting the commit merges
    """
    commits_b = subprocess.check_output(["git", "log", "--no-merges", "--pretty=%H", LANGUAGES_PATH], stderr=DEVNULL)
    commits_reverse = commits_b.decode().strip().split('\n')

    return commits_reverse[::-1]


def languages_lang_file():
    """
    Returns the list of languages present in the language file
    with their respective type and group
    """
    yaml = read_langs_file()

    return list(yaml.keys())

def read_langs_file():
    """
    Reads the language file
    """
    with open(LANGUAGES_PATH) as langs_file:
        try:
            languages_yaml = yaml.load(langs_file)
            return languages_yaml
        except:
            return {}


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


def store(languages):
    """
    Stores in database the result.
    If the result is equal to the latest row in the db
    it only updates the timestamp
    """
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


if __name__ == "__main__":
    sys.exit(main())
