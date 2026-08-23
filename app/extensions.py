"""
Shared extension objects.

These live in their own file so that models and controllers can import
`db` without importing the app factory (which would cause a circular
import). This is the standard Flask pattern.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
