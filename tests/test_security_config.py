import pytest

from src import config


def test_development_allows_local_configuration(monkeypatch):
    monkeypatch.setattr(config, "APP_ENV", "development")
    monkeypatch.setattr(config, "APP_DEBUG", True)
    monkeypatch.setattr(config, "JWT_SECRET", "development-only-change-me")
    monkeypatch.setattr(config, "ADMIN_EMAIL", "")
    monkeypatch.setattr(config, "ADMIN_PASSWORD", "")

    config.validate_security_config()


def test_production_rejects_development_credentials(monkeypatch):
    monkeypatch.setattr(config, "APP_ENV", "production")
    monkeypatch.setattr(config, "APP_DEBUG", True)
    monkeypatch.setattr(config, "JWT_SECRET", "development-only-change-me")
    monkeypatch.setattr(config, "ADMIN_EMAIL", "")
    monkeypatch.setattr(config, "ADMIN_PASSWORD", "short")

    with pytest.raises(RuntimeError, match="Invalid production security configuration"):
        config.validate_security_config()


def test_production_accepts_strong_configuration(monkeypatch):
    monkeypatch.setattr(config, "APP_ENV", "production")
    monkeypatch.setattr(config, "APP_DEBUG", False)
    monkeypatch.setattr(config, "JWT_SECRET", "x" * 64)
    monkeypatch.setattr(config, "ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setattr(config, "ADMIN_PASSWORD", "strong-password-2026")

    config.validate_security_config()
