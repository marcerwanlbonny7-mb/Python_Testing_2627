import copy

import pytest

from server import app, bookings, clubs, competitions


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
    yield
    clubs.clear()
    clubs.extend(clubs_snapshot)
    competitions.clear()
    competitions.extend(competitions_snapshot)
    bookings.clear()
    bookings.update(bookings_snapshot)
