# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["EventSearchResponse", "Data"]


class Data(BaseModel):
    id: str
    """A unique value, generated by the client, that is used to de-duplicate events.

    Exactly one event with a given idempotency key will be ingested, which allows
    for safe request retries.
    """

    customer_id: Optional[str] = None
    """The Orb Customer identifier"""

    deprecated: bool
    """A boolean indicating whether the event is currently deprecated."""

    event_name: str
    """A name to meaningfully identify the action or event type."""

    external_customer_id: Optional[str] = None
    """
    An alias for the Orb customer, whose mapping is specified when creating the
    customer
    """

    properties: object
    """A dictionary of custom properties.

    Values in this dictionary must be numeric, boolean, or strings. Nested
    dictionaries are disallowed.
    """

    timestamp: datetime
    """An ISO 8601 format date with no timezone offset (i.e.

    UTC). This should represent the time that usage was recorded, and is
    particularly important to attribute usage to a given billing period.
    """


class EventSearchResponse(BaseModel):
    data: List[Data]
