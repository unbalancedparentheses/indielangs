import pytest
import gitlog

def test_len():
    len_languages = len(gitlog.languages())

    gitlog.prepare()
    len_file = len(gitlog.lang_keys())
    gitlog.clean()

    assert len_languages == len_file


def test_keys():
    langs_list = sorted([lang['name'] for lang in gitlog.languages()])

    gitlog.prepare()
    langs_file_list = sorted(gitlog.lang_keys())
    gitlog.clean()

    assert langs_list == langs_file_list
