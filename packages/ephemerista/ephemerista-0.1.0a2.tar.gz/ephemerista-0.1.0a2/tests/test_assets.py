import uuid

from ephemerista.assets import asset_id


def test_asset_id(lunar_scenario):
    expected = uuid.UUID("8c8e6427-7012-495b-b83a-214e220c5e74")
    asset = lunar_scenario["CEBR"]
    assert asset_id(asset) == expected
    assert asset_id(asset.asset_id) == expected
