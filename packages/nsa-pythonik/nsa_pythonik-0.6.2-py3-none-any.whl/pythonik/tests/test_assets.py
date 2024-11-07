import uuid

import requests_mock

from pythonik.client import PythonikClient
from pythonik.models.assets.assets import Asset, AssetCreate
from pythonik.models.assets.segments import SegmentBody, SegmentResponse
from pythonik.specs.assets import (
    BASE,
    GET_URL,
    AssetSpec,
    SEGMENT_URL,
    SEGMENT_URL_UPDATE,
)


def test_partial_update_asset():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Asset()
        data = model.model_dump()
        mock_address = AssetSpec.gen_url(GET_URL.format(asset_id))

        m.patch(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.assets().partial_update_asset(asset_id=asset_id, body=model)


def test_get_asset():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Asset()
        data = model.model_dump()
        mock_address = AssetSpec.gen_url(GET_URL.format(asset_id))

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.assets().get(asset_id=asset_id)


def test_create_asset():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_title = str(uuid.uuid4())

        model = AssetCreate(title=asset_title)
        data = model.model_dump()
        mock_address = AssetSpec.gen_url(BASE)

        m.post(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.assets().create(body=model)


def test_create_segment():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = SegmentBody()
        response = SegmentResponse()
        data = response.model_dump()
        mock_address = AssetSpec.gen_url(SEGMENT_URL.format(asset_id))

        m.post(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.assets().create_segment(asset_id=asset_id, body=model)


def test_update_segment():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        segment_id = str(uuid.uuid4())

        model = SegmentBody()
        response = SegmentResponse()
        data = response.model_dump()
        mock_address = AssetSpec.gen_url(
            SEGMENT_URL_UPDATE.format(asset_id, segment_id)
        )

        m.put(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.assets().update_segment(
            asset_id=asset_id, segment_id=segment_id, body=model
        )


def test_partial_update_segment():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        segment_id = str(uuid.uuid4())

        model = SegmentBody()
        response = SegmentResponse()
        data = response.model_dump()
        mock_address = AssetSpec.gen_url(
            SEGMENT_URL_UPDATE.format(asset_id, segment_id)
        )

        m.patch(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.assets().partial_update_segment(
            asset_id=asset_id, segment_id=segment_id, body=model
        )
