"""
Configuration for every environment.

Never put real secrets in this file. Put them in a .env file (which git
ignores) and read them here with os.environ.get(). See .env.example.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class BaseConfig:
    """Settings shared by every environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Where form submissions are stored.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'thebeautycast.db'}",
    )

    # Shown in the page footer and <title>.
    SITE_NAME = "The Beauty Cast"


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    # Render and most hosts hand you a postgres:// URL; SQLAlchemy needs
    # postgresql://. This rewrites it automatically.
    _url = os.environ.get("DATABASE_URL", "")
    if _url.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = _url.replace("postgres://", "postgresql://", 1)


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


_CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(name: str | None = None):
    """Return the config class for the given environment name."""
    name = name or os.environ.get("FLASK_ENV", "development")
    return _CONFIGS.get(name, DevelopmentConfig)
