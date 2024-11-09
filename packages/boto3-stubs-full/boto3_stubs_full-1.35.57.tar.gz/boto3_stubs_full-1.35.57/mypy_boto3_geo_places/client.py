"""
Type annotations for geo-places service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_geo_places.client import LocationServicePlacesV2Client

    session = Session()
    client: LocationServicePlacesV2Client = session.client("geo-places")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AutocompleteRequestRequestTypeDef,
    AutocompleteResponseTypeDef,
    GeocodeRequestRequestTypeDef,
    GeocodeResponseTypeDef,
    GetPlaceRequestRequestTypeDef,
    GetPlaceResponseTypeDef,
    ReverseGeocodeRequestRequestTypeDef,
    ReverseGeocodeResponseTypeDef,
    SearchNearbyRequestRequestTypeDef,
    SearchNearbyResponseTypeDef,
    SearchTextRequestRequestTypeDef,
    SearchTextResponseTypeDef,
    SuggestRequestRequestTypeDef,
    SuggestResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("LocationServicePlacesV2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LocationServicePlacesV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServicePlacesV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#exceptions)
        """

    def autocomplete(
        self, **kwargs: Unpack[AutocompleteRequestRequestTypeDef]
    ) -> AutocompleteResponseTypeDef:
        """
        The autocomplete operation speeds up and increases the accuracy of entering
        addresses by providing a list of address candidates matching a partially
        entered
        address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.autocomplete)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#autocomplete)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#close)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#generate_presigned_url)
        """

    def geocode(self, **kwargs: Unpack[GeocodeRequestRequestTypeDef]) -> GeocodeResponseTypeDef:
        """
        The `Geocode` action allows you to obtain coordinates, addresses, and other
        information about
        places.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.geocode)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#geocode)
        """

    def get_place(self, **kwargs: Unpack[GetPlaceRequestRequestTypeDef]) -> GetPlaceResponseTypeDef:
        """
        Finds a place by its unique ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.get_place)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#get_place)
        """

    def reverse_geocode(
        self, **kwargs: Unpack[ReverseGeocodeRequestRequestTypeDef]
    ) -> ReverseGeocodeResponseTypeDef:
        """
        The `ReverseGeocode` operation allows you to retrieve addresses and place
        information from
        coordinates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.reverse_geocode)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#reverse_geocode)
        """

    def search_nearby(
        self, **kwargs: Unpack[SearchNearbyRequestRequestTypeDef]
    ) -> SearchNearbyResponseTypeDef:
        """
        Search nearby a specified location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.search_nearby)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#search_nearby)
        """

    def search_text(
        self, **kwargs: Unpack[SearchTextRequestRequestTypeDef]
    ) -> SearchTextResponseTypeDef:
        """
        Use the `SearchText` operation to search for geocode and place information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.search_text)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#search_text)
        """

    def suggest(self, **kwargs: Unpack[SuggestRequestRequestTypeDef]) -> SuggestResponseTypeDef:
        """
        The `Suggest` operation finds addresses or place candidates based on incomplete
        or misspelled
        queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client.suggest)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#suggest)
        """
