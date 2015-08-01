"""
Work with the languages github repo
"""

import os
import shutil
import subprocess
import yaml


DEVNULL = open(os.devnull, 'wb')
LANGUAGES_REPO = "https://github.com/github/linguist.git"
REPO_DIR = "/tmp/linguist"
LANGUAGES_PATH = "./lib/linguist/languages.yml"


def languages():
    """
    Obtain the dates where each language support was added
    and the metadata associated with it. Sort the list of
    languages with their respective dates and metadata.
    """
    prepare()
    dates_info = dates()
    metadata_info = metadata()
    langs = []

    for lang in metadata_info:
        aux = {}
        aux['name'] = lang
        aux['timestamp'] = dates_info[lang]

        if metadata_info[lang].get('type', None):
            aux['type'] = metadata_info[lang]['type']
        if metadata_info[lang].get('group', None):
            aux['group'] = metadata_info[lang]['group']

        langs.append(aux)

    sorted_languages = sorted(langs,
                              key=lambda lang: lang["timestamp"],
                              reverse=True)
    clean()
    return sorted_languages


def prepare():
    """
    Clone the linguist repo and change the working directory to it.
    It also deletes the linguist directory it if was already present.
    """
    clean()
    subprocess.call(["git", "clone", LANGUAGES_REPO, REPO_DIR],
                    stdout=DEVNULL, stderr=DEVNULL)
    os.chdir(REPO_DIR)


def clean():
    """
    Return to the previous working directory and remove the linguist directory.
    """
    if os.path.exists(REPO_DIR):
        os.chdir("/")
        shutil.rmtree(REPO_DIR)


def dates():
    """
    Return the list of languages available in the language file
    with the date in which it was added.
    """
    language_history = set()
    result = {}

    for i, commit in enumerate(commits()):
        actual = langs_in_commit(commit)

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
    return filtered


def metadata():
    """
    Return the type and group metadata for each language
    """
    languages = read_langs_file()
    metadata_keys = ('type', 'group')

    result = {}

    for language in languages:
        result[language] = {k: languages[language][k]
                            for k in languages[language]
                            if k in metadata_keys}
    return result


def commits():
    """
    Return the list of commits in ascending order that changed
    the languages file without counting the commit merges.
    """
    commits_b = subprocess.check_output(["git", "log",
                                         "--no-merges", "--pretty=%H",
                                         LANGUAGES_PATH],
                                        stderr=DEVNULL)
    commits_reverse = commits_b.decode().strip().split('\n')
    return commits_reverse[::-1]


def lang_keys():
    """
    Return the list of languages present in the language file
    with their respective type and group.
    """
    languages = read_langs_file()
    return list(languages.keys())


def read_langs_file():
    """
    Reads the language file.
    """
    with open(LANGUAGES_PATH) as langs_file:
        try:
            languages_yaml = yaml.load(langs_file)
            return languages_yaml
        except:
            return {}


def langs_in_commit(commit):
    """
    Return the list of languages
    present in the language file for a specific commit.
    """
    subprocess.call(["git", "checkout", commit, LANGUAGES_PATH],
                    stdout=DEVNULL, stderr=DEVNULL)
    return lang_keys()


def commit_time(commit):
    """
    Return the commit time in epoc format of a specific commit.
    """
    output_b = subprocess.check_output(["git", "show", "-s", "--format=%ct",
                                        commit])
    output = output_b.decode().strip()
    return int(output)


def filter_deleted(languages):
    """
    Return a hash with the languages that are in the languages argument
    minus the ones that are no longer present in the last commit.
    """
    subprocess.call(["git", "reset", "--hard", "master"],
                    stdout=DEVNULL, stderr=DEVNULL)
    last_languages = lang_keys()

    filtered_languages = {}

    for lang in languages:
        if lang in last_languages:
            filtered_languages[lang] = languages[lang]

    return filtered_languages
