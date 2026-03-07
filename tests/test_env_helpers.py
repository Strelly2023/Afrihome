# tests/test_env_helpers.py
import os
import importlib

def test_env_str_with_default(tmp_path, monkeypatch):
    monkeypatch.delenv("DJANGO_SECRET_KEY", raising=False)
    # reload ensures functions pick up monkeypatched env
    base = importlib.import_module("config.settings.base")
    assert base.env_str("MISSING_OK", "fallback") == "fallback"

def test_env_str_required_raises(monkeypatch):
    from config.settings import base
    monkeypatch.delenv("REQUIRED", raising=False)
    try:
        base.env_str("REQUIRED")
        assert False, "expected RuntimeError"
    except RuntimeError:
        assert True

def test_env_bool_truthy(monkeypatch):
    from config.settings import base
    monkeypatch.setenv("FLAG", "TrUe")
    assert base.env_bool("FLAG", False) is True

def test_env_int(monkeypatch):
    from config.settings import base
    monkeypatch.setenv("NUM", "42")
    assert base.env_int("NUM", 1) == 42