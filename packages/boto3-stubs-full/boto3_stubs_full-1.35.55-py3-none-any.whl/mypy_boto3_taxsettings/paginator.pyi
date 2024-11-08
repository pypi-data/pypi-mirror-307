"""
Type annotations for taxsettings service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_taxsettings/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_taxsettings.client import TaxSettingsClient
    from mypy_boto3_taxsettings.paginator import (
        ListSupplementalTaxRegistrationsPaginator,
        ListTaxRegistrationsPaginator,
    )

    session = Session()
    client: TaxSettingsClient = session.client("taxsettings")

    list_supplemental_tax_registrations_paginator: ListSupplementalTaxRegistrationsPaginator = client.get_paginator("list_supplemental_tax_registrations")
    list_tax_registrations_paginator: ListTaxRegistrationsPaginator = client.get_paginator("list_tax_registrations")
    ```
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListSupplementalTaxRegistrationsRequestListSupplementalTaxRegistrationsPaginateTypeDef,
    ListSupplementalTaxRegistrationsResponseTypeDef,
    ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef,
    ListTaxRegistrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListSupplementalTaxRegistrationsPaginator", "ListTaxRegistrationsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSupplementalTaxRegistrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Paginator.ListSupplementalTaxRegistrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_taxsettings/paginators/#listsupplementaltaxregistrationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSupplementalTaxRegistrationsRequestListSupplementalTaxRegistrationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSupplementalTaxRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Paginator.ListSupplementalTaxRegistrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_taxsettings/paginators/#listsupplementaltaxregistrationspaginator)
        """

class ListTaxRegistrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Paginator.ListTaxRegistrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_taxsettings/paginators/#listtaxregistrationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef]
    ) -> _PageIterator[ListTaxRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings.html#TaxSettings.Paginator.ListTaxRegistrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_taxsettings/paginators/#listtaxregistrationspaginator)
        """
