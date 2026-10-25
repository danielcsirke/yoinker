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


def test_advanced_fills_defaults_and_drops_garbage():
    from yoinker.config import ADVANCED_DEFAULTS
    assert config.advanced({}) == ADVANCED_DEFAULTS
    got = config.advanced({"advanced": {"codec": "best", "thumbnail": "yes", "rate_limit": 5}})
    assert got["codec"] == "best"
    assert got["thumbnail"] is False      # wrong type -> default
    assert got["rate_limit"] == ""        # wrong type -> default
    assert config.advanced({"advanced": "nonsense"}) == ADVANCED_DEFAULTS
