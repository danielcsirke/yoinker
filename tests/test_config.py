from yoinker import config


def test_roundtrip(tmp_path):
    p = tmp_path / "sub" / "settings.json"
    config.save({"language": "hu", "folder": "/x"}, p)
    assert config.load(p) == {"language": "hu", "folder": "/x"}


def test_missing_and_broken_files_are_empty(tmp_path):
    assert config.load(tmp_path / "nope.json") == {}
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert config.load(bad) == {}
    bad.write_text("[1,2]")
    assert config.load(bad) == {}


def test_default_dir_is_in_downloads():
    assert config.default_download_dir().name == "Yoinker"
    assert config.default_download_dir().parent.name == "Downloads"
