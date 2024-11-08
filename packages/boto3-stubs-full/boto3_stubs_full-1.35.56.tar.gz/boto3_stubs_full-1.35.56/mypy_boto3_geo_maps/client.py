"""
Type annotations for geo-maps service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_geo_maps.client import LocationServiceMapsV2Client

    session = Session()
    client: LocationServiceMapsV2Client = session.client("geo-maps")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    GetGlyphsRequestRequestTypeDef,
    GetGlyphsResponseTypeDef,
    GetSpritesRequestRequestTypeDef,
    GetSpritesResponseTypeDef,
    GetStaticMapRequestRequestTypeDef,
    GetStaticMapResponseTypeDef,
    GetStyleDescriptorRequestRequestTypeDef,
    GetStyleDescriptorResponseTypeDef,
    GetTileRequestRequestTypeDef,
    GetTileResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("LocationServiceMapsV2Client",)


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


class LocationServiceMapsV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceMapsV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#close)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#generate_presigned_url)
        """

    def get_glyphs(
        self, **kwargs: Unpack[GetGlyphsRequestRequestTypeDef]
    ) -> GetGlyphsResponseTypeDef:
        """
        Returns the map's glyphs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.get_glyphs)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#get_glyphs)
        """

    def get_sprites(
        self, **kwargs: Unpack[GetSpritesRequestRequestTypeDef]
    ) -> GetSpritesResponseTypeDef:
        """
        Returns the map's sprites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.get_sprites)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#get_sprites)
        """

    def get_static_map(
        self, **kwargs: Unpack[GetStaticMapRequestRequestTypeDef]
    ) -> GetStaticMapResponseTypeDef:
        """
        Provides high-quality static map images with customizable options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.get_static_map)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#get_static_map)
        """

    def get_style_descriptor(
        self, **kwargs: Unpack[GetStyleDescriptorRequestRequestTypeDef]
    ) -> GetStyleDescriptorResponseTypeDef:
        """
        Returns information about the style.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.get_style_descriptor)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#get_style_descriptor)
        """

    def get_tile(self, **kwargs: Unpack[GetTileRequestRequestTypeDef]) -> GetTileResponseTypeDef:
        """
        Returns a tile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client.get_tile)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/client/#get_tile)
        """
