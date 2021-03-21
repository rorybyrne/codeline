import re

from codeline.sdk.util import regex


def test_successful_parse_command():
    s = "# <| git commit -m 'howdy'"
    s2 = "    # <| git commit -m 'howdy'"
    regexp = re.compile(regex.PYTHON)

    r = regexp.search(s)
    assert r is not None and r.group(1) == "git"
    r2 = regexp.search(s2)
    assert r2 is not None and r2.group(1) == "git"


def test_failure_parse_bad_commands():
    s = "# git commit -m 'howdy'"
    s2 = "#git commit -m 'howdy'"
    s3 = "# git <| commit -m 'howdy'"
    s4 = "# <|"
    s5 = "# <| "
    s6 = "# <|  "
    regexp = re.compile(regex.PYTHON)

    assert not regexp.search(s)
    assert not regexp.search(s2)
    assert not regexp.search(s3)
    assert not regexp.search(s4)
    assert not regexp.search(s5)
    assert not regexp.search(s6)


def test_extract_command_success():
    line = "    # <| echo 'howdy'"
    command, options = regex.extract_command_and_tail(line)
    assert command == "echo"
    assert options == "'howdy'"
