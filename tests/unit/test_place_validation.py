import re

VALID_CLUB = "Simply Lift"
VALID_COMPETITION = "Spring Festival"
FULL_COMPETITION = "Fall Classic"


def places_available(client, competition, club):
    response = client.get(f"/book/{competition}/{club}")
    match = re.search(r"Places available: (\d+)", response.data.decode())
    return int(match.group(1))


def book_places(client, competition, club, places):
    return client.post(
        "/purchasePlaces",
        data={"competition": competition, "club": club, "places": places},
        follow_redirects=True,
    )


class TestPlaceValidation:
    def test_valid_booking_reduces_available_places(self, client):
        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "3")

        assert response.status_code == 200
        assert b"booking complete" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 22

    def test_booking_exactly_12_places_is_accepted(self, client):
        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "12")

        assert response.status_code == 200
        assert b"booking complete" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 13

    def test_negative_places_are_rejected(self, client):
        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "-5")

        assert b"Invalid number of places" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 25

    def test_zero_places_are_rejected(self, client):
        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "0")

        assert b"Invalid number of places" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 25

    def test_non_numeric_places_do_not_crash(self, client):
        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "abc")

        assert response.status_code == 200
        assert b"Invalid number of places" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 25

    def test_more_than_12_places_are_rejected(self, client):
        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "13")

        assert b"Cannot book more than 12 places" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 25

    def test_more_places_than_available_are_rejected(self, client):
        from server import competitions

        competition = next(
            c for c in competitions if c["name"] == FULL_COMPETITION
        )
        competition["numberOfPlaces"] = "5"

        response = book_places(client, FULL_COMPETITION, VALID_CLUB, "6")

        assert b"Not enough places available" in response.data
        assert places_available(client, FULL_COMPETITION, VALID_CLUB) == 5


class TestCumulativeTwelveLimit:
    def test_two_bookings_cannot_exceed_12_in_total(self, client):
        book_places(client, VALID_COMPETITION, VALID_CLUB, "8")

        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "8")

        assert b"Cannot book more than 12 places" in response.data

    def test_bookings_up_to_exactly_12_are_accepted(self, client):
        book_places(client, VALID_COMPETITION, VALID_CLUB, "8")

        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "4")

        assert b"booking complete" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 13

    def test_booking_beyond_cumulative_12_is_rejected(self, client):
        book_places(client, VALID_COMPETITION, VALID_CLUB, "8")
        book_places(client, VALID_COMPETITION, VALID_CLUB, "4")

        response = book_places(client, VALID_COMPETITION, VALID_CLUB, "1")

        assert b"Cannot book more than 12 places" in response.data
        assert places_available(client, VALID_COMPETITION, VALID_CLUB) == 13

    def test_limit_is_per_competition_not_global(self, client):
        book_places(client, VALID_COMPETITION, VALID_CLUB, "12")

        response = book_places(client, FULL_COMPETITION, VALID_CLUB, "1")

        assert b"booking complete" in response.data
        assert places_available(client, FULL_COMPETITION, VALID_CLUB) == 12
