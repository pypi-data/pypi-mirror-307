"""
Type annotations for geo-routes service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_geo_routes.client import LocationServiceRoutesV2Client

    session = Session()
    client: LocationServiceRoutesV2Client = session.client("geo-routes")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CalculateIsolinesRequestRequestTypeDef,
    CalculateIsolinesResponseTypeDef,
    CalculateRouteMatrixRequestRequestTypeDef,
    CalculateRouteMatrixResponseTypeDef,
    CalculateRoutesRequestRequestTypeDef,
    CalculateRoutesResponseTypeDef,
    OptimizeWaypointsRequestRequestTypeDef,
    OptimizeWaypointsResponseTypeDef,
    SnapToRoadsRequestRequestTypeDef,
    SnapToRoadsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("LocationServiceRoutesV2Client",)


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


class LocationServiceRoutesV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceRoutesV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#exceptions)
        """

    def calculate_isolines(
        self, **kwargs: Unpack[CalculateIsolinesRequestRequestTypeDef]
    ) -> CalculateIsolinesResponseTypeDef:
        """
        Use the `CalculateIsolines` action to find service areas that can be reached in
        a given threshold of time,
        distance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.calculate_isolines)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#calculate_isolines)
        """

    def calculate_route_matrix(
        self, **kwargs: Unpack[CalculateRouteMatrixRequestRequestTypeDef]
    ) -> CalculateRouteMatrixResponseTypeDef:
        """
        Calculates route matrix containing the results for all pairs of Origins to
        Destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.calculate_route_matrix)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#calculate_route_matrix)
        """

    def calculate_routes(
        self, **kwargs: Unpack[CalculateRoutesRequestRequestTypeDef]
    ) -> CalculateRoutesResponseTypeDef:
        """
        Calculates a route given the following required parameters: `Origin` and
        `Destination`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.calculate_routes)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#calculate_routes)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#close)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#generate_presigned_url)
        """

    def optimize_waypoints(
        self, **kwargs: Unpack[OptimizeWaypointsRequestRequestTypeDef]
    ) -> OptimizeWaypointsResponseTypeDef:
        """
        Calculates the optimal order to travel between a set of waypoints to minimize
        either the travel time or the distance travelled during the journey, based on
        road network restrictions and the traffic pattern
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.optimize_waypoints)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#optimize_waypoints)
        """

    def snap_to_roads(
        self, **kwargs: Unpack[SnapToRoadsRequestRequestTypeDef]
    ) -> SnapToRoadsResponseTypeDef:
        """
        The SnapToRoads action matches GPS trace to roads most likely traveled on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client.snap_to_roads)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/client/#snap_to_roads)
        """
