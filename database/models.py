"""Aggregate imports so Alembic can discover models.

This module is imported by migration tooling; symbols appear unused to pylint.
"""
# pylint: disable=unused-import
from database import base
from database.channel_static import channel_static
from database.channel_dynamic import channel_dynamic
