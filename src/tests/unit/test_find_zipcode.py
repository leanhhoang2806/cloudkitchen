from src.media.long_lat.longitude_lattitude_reader import ZipcodeSearchReader
import pytest


@pytest.fixture
def zipcode_manager():
    return ZipcodeSearchReader()


def test_find_neighbors(zipcode_manager):
    target_zip = 75025
    neighbors_within_50_km = zipcode_manager.find_neighbors(target_zip)
    assert len(neighbors_within_50_km) == 144
