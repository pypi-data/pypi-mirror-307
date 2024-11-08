from pythonik.models.assets.assets import Asset, AssetCreate
from pythonik.models.assets.segments import SegmentBody, SegmentResponse
from pythonik.models.base import Response
from pythonik.specs.base import Spec

BASE = "assets"
GET_URL = BASE + "/{}/"
SEGMENT_URL = BASE + "/{}/segments/"
SEGMENT_URL_UPDATE = SEGMENT_URL + "{}/"


class AssetSpec(Spec):
    server = "API/assets/"

    def partial_update_asset(
        self, asset_id: str, body: Asset, exclude_defaults=True, **kwargs
    ) -> Response:
        """Partially update an asset using PATCH"""
        response = self._patch(
            GET_URL.format(asset_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )
        return self.parse_response(response, Asset)

    def get(self, asset_id: str) -> Response:
        """
        Get an iconik asset by id
        Returns: Response(model=Asset)
        """

        resp = self._get(GET_URL.format(asset_id))

        return self.parse_response(resp, Asset)

    def create(self, body: AssetCreate, exclude_defaults=True, **kwargs) -> Response:
        """
        Create a new asset
        Returns: Response(model=Asset)
        """
        response = self._post(
            BASE, json=body.model_dump(exclude_defaults=exclude_defaults), **kwargs
        )
        return self.parse_response(response, Asset)

    def create_segment(
        self, asset_id: str, body: SegmentBody, exclude_defaults=True, **kwargs
    ) -> Response:
        """
        Create a segment on an asset, such as a comment
        Returns: Response(model=SegmentResponse)
        """

        resp = self._post(
            SEGMENT_URL.format(asset_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )

        return self.parse_response(resp, SegmentResponse)

    def update_segment(
        self,
        asset_id: str,
        segment_id: str,
        body: SegmentBody,
        exclude_defaults=True,
        **kwargs
    ) -> Response:
        """
        Update a segment on an asset, such as a comment, using PUT
        Returns: Response(model=SegmentResponse)

        PUT

        Full Update: PUT is used to update a resource by replacing it with the new data provided in the request.
        It usually requires sending the complete representation of the resource.

        Idempotent: If you perform the same PUT request multiple times,
        the result will be the same. It will replace the resource with the same data every time.

        Complete Resource: Typically, a PUT request contains the entire resource.
        If any fields are omitted in the request, those fields are typically reset to their default values or removed.


        """

        resp = self._put(
            SEGMENT_URL_UPDATE.format(asset_id, segment_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )

        return self.parse_response(resp, SegmentResponse)

    def partial_update_segment(
        self,
        asset_id: str,
        segment_id: str,
        body: SegmentBody,
        exclude_defaults=True,
        **kwargs
    ) -> Response:
        """
        Partially Update a segment on an asset, such as a comment, using PATCH
        Returns: Response(model=SegmentResponse)

        PATCH
            Partial Update: PATCH is used for partial updates. It allows you to send only the fields that need to be updated,
            leaving the rest of the resource unchanged.

            Not Necessarily Idempotent: While PATCH can be idempotent, it's not guaranteed to be. Multiple identical PATCH requests could result in different states
            if the updates depend on the current state of the resource.

            Sparse Representation: A PATCH request typically contains only the fields that need to be modified.
        """

        resp = self._patch(
            SEGMENT_URL_UPDATE.format(asset_id, segment_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )

        return self.parse_response(resp, SegmentResponse)
