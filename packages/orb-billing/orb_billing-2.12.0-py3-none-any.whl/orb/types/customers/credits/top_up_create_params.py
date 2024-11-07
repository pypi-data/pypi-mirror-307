# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["TopUpCreateParams", "InvoiceSettings"]


class TopUpCreateParams(TypedDict, total=False):
    amount: Required[str]
    """The amount to increment when the threshold is reached."""

    currency: Required[str]
    """The currency or custom pricing unit to use for this top-up.

    If this is a real-world currency, it must match the customer's invoicing
    currency.
    """

    invoice_settings: Required[InvoiceSettings]
    """Settings for invoices generated by triggered top-ups."""

    per_unit_cost_basis: Required[str]
    """How much, in the customer's currency, to charge for each unit."""

    threshold: Required[str]
    """The threshold at which to trigger the top-up.

    If the balance is at or below this threshold, the top-up will be triggered.
    """

    expires_after: Optional[int]
    """The number of days or months after which the top-up expires.

    If unspecified, it does not expire.
    """

    expires_after_unit: Optional[Literal["day", "month"]]
    """The unit of expires_after."""


class InvoiceSettings(TypedDict, total=False):
    auto_collection: Required[bool]
    """
    Whether the credits purchase invoice should auto collect with the customer's
    saved payment method.
    """

    net_terms: Required[int]
    """
    The net terms determines the difference between the invoice date and the issue
    date for the invoice. If you intend the invoice to be due on issue, set this
    to 0.
    """

    memo: Optional[str]
    """An optional memo to display on the invoice."""

    require_successful_payment: bool
    """
    If true, new credit blocks created by this top-up will require that the
    corresponding invoice is paid before they can be drawn down from.
    """
