import pytest

VALID_CLUB = "Simply Lift"
VALID_EMAIL = "john@simplylift.co"
VALID_COMPETITION = "Spring Festival"
FAKE_NAME = "Nonexistent Thing"


@pytest.fixture(autouse=True)
def login(client):
    client.post("/showSummary", data={"email": VALID_EMAIL})


class TestPurchasePlaces:
    def test_valid_booking_returns_welcome_page(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": VALID_COMPETITION,
                "club": VALID_CLUB,
                "places": "2",
            },
        )

        assert response.status_code == 200
        assert b"booking complete" in response.data

    def test_unknown_competition_does_not_crash(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": FAKE_NAME,
                "club": VALID_CLUB,
                "places": "2",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

    def test_unknown_club_does_not_crash(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": VALID_COMPETITION,
                "club": FAKE_NAME,
                "places": "2",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

    def test_unknown_competition_shows_error_message(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": FAKE_NAME,
                "club": VALID_CLUB,
                "places": "2",
            },
            follow_redirects=True,
        )

        assert b"Something went wrong" in response.data

    def test_unknown_club_shows_error_message(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": VALID_COMPETITION,
                "club": FAKE_NAME,
                "places": "2",
            },
            follow_redirects=True,
        )

        assert b"only make bookings for your own club" in response.data
