from yoinker.i18n import LANGUAGES, STRINGS, classify_error, tr


def test_every_language_has_every_key():
    keys = set(STRINGS["en"])
    for lang in LANGUAGES:
        assert set(STRINGS[lang]) == keys, f"{lang} is missing/has extra keys"


def test_placeholders_match_between_languages():
    import re

    for key, en_text in STRINGS["en"].items():
        en_fields = set(re.findall(r"\{(\w+)\}", en_text))
        for lang in LANGUAGES:
            fields = set(re.findall(r"\{(\w+)\}", STRINGS[lang][key]))
            assert fields == en_fields, f"{lang}.{key} placeholders differ"


def test_tr_formats_and_falls_back():
    assert "7" in tr("en", "eta", seconds=7)
    assert tr("hu", "download") == "LETÖLTÉS"
    assert tr("xx", "download") == tr("en", "download")
    assert tr("en", "no_such_key") == "no_such_key"


def test_classify_error_known_cases():
    assert classify_error("ERROR: Private video. Sign in if you've been granted access") == "err_login"
    assert classify_error("ERROR: [youtube] abc: Video unavailable") == "err_unavailable"
    assert classify_error("Unsupported URL: https://example.com") == "err_unsupported"
    assert classify_error("urlopen error [Errno -3] Temporary failure in name resolution") == "err_network"
    assert classify_error("HTTP Error 403: Forbidden") == "err_blocked"
    assert classify_error("ffmpeg not found") == "err_ffmpeg"
    assert classify_error("[Errno 28] No space left on device") == "err_disk"
    assert classify_error("The uploader has not made this video available in your country") == "err_geo"
    assert classify_error("something totally weird") == "err_generic"
