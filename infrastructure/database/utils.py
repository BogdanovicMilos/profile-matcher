from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime


class TimestampsMixin:
    """
    Mixin to create timestamp fields for creation, update, and deletion
    """

    created = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
    )
    deleted = Column(DateTime(timezone=True), default=None)
    modified = Column(DateTime(timezone=True), default=None)

    def delete(self):
        """
        Mixin method to set timestamp for deletion
        """
        self.deleted = datetime.now(timezone.utc)

    def update(self):
        """
        Mixin method to set timestamp for update
        """
        self.modified = datetime.now(timezone.utc)
