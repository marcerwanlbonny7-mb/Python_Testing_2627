import copy
from pathlib import Path

import pytest

from server import app, bookings, clubs, competitions

JSON_FILES = ('clubs.json', 'competitions.json', 'bookings.json')


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_data():
    clubs_snapshot = copy.deepcopy(clubs)
    competitions_snapshot = copy.deepcopy(competitions)
    bookings_snapshot = bookings.copy()
    disk_snapshot = {}
    for name in JSON_FILES:
        path = Path(name)
        disk_snapshot[name] = path.read_bytes() if path.exists() else None
    yield
    clubs.clear()
    clubs.extend(clubs_snapshot)
    competitions.clear()
    competitions.extend(competitions_snapshot)
    bookings.clear()
    bookings.update(bookings_snapshot)
    for name, content in disk_snapshot.items():
        path = Path(name)
        if content is None:
            if path.exists():
                path.unlink()
        else:
            path.write_bytes(content)
