import pytest

from notes import read_file, word_count


def test_word_count():
    assert word_count("one two  three\nfour") == 4
    assert word_count("") == 0


def test_read_file(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("héllo world", encoding="utf-8")
    assert read_file(str(f)) == "héllo world"


def test_read_file_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_file(str(tmp_path / "nope.txt"))
