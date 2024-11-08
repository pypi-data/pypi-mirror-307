"""
Main interface for taxsettings service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_taxsettings import (
        Client,
        ListSupplementalTaxRegistrationsPaginator,
        ListTaxRegistrationsPaginator,
        TaxSettingsClient,
    )

    session = Session()
    client: TaxSettingsClient = session.client("taxsettings")

    list_supplemental_tax_registrations_paginator: ListSupplementalTaxRegistrationsPaginator = client.get_paginator("list_supplemental_tax_registrations")
    list_tax_registrations_paginator: ListTaxRegistrationsPaginator = client.get_paginator("list_tax_registrations")
    ```
"""

from .client import TaxSettingsClient
from .paginator import ListSupplementalTaxRegistrationsPaginator, ListTaxRegistrationsPaginator

Client = TaxSettingsClient


__all__ = (
    "Client",
    "ListSupplementalTaxRegistrationsPaginator",
    "ListTaxRegistrationsPaginator",
    "TaxSettingsClient",
)
