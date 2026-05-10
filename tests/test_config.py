import importlib
import sys


def test_config_reads_env_vars(monkeypatch):
    monkeypatch.setenv("WP_URL", "http://test.local")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-key")
    monkeypatch.setenv("USE_WPCLI", "false")

    if "scripts.config" in sys.modules:
        del sys.modules["scripts.config"]

    import scripts.config as config
    importlib.reload(config)

    assert config.WP_URL == "http://test.local"
    assert config.ANTHROPIC_API_KEY == "sk-test-key"
    assert config.USE_WPCLI is False


def test_config_use_wpcli_defaults_true(monkeypatch):
    monkeypatch.delenv("USE_WPCLI", raising=False)

    if "scripts.config" in sys.modules:
        del sys.modules["scripts.config"]

    import scripts.config as config
    importlib.reload(config)

    assert config.USE_WPCLI is True
