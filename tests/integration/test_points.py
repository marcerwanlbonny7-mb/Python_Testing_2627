RICH_CLUB = "Simply Lift"
RICH_EMAIL = "john@simplylift.co"
POOR_CLUB = "Iron Temple"
POOR_EMAIL = "admin@irontemple.com"
VALID_COMPETITION = "Spring Festival"
CLUB_EMAILS = {
    "Simply Lift": "john@simplylift.co",
    "Iron Temple": "admin@irontemple.com",
    "She Lifts": "kate@shelifts.co.uk",
}


def book_places(client, competition, club, places):
    client.post("/showSummary", data={"email": CLUB_EMAILS[club]})
    return client.post(
        "/purchasePlaces",
        data={"competition": competition, "club": club, "places": places},
        follow_redirects=True,
    )


def login(client, email):
    return client.post(
        "/showSummary", data={"email": email}, follow_redirects=True
    )


class TestPointsDeduction:
    def test_booking_deducts_points_from_club(self, client):
        response = book_places(client, VALID_COMPETITION, RICH_CLUB, "3")

        assert response.status_code == 200
        assert b"booking complete" in response.data
        response = login(client, RICH_EMAIL)
        assert b"Points available: 10" in response.data

    def test_booking_can_drain_balance_to_zero(self, client):
        response = book_places(client, VALID_COMPETITION, POOR_CLUB, "4")

        assert response.status_code == 200
        assert b"booking complete" in response.data
        response = login(client, POOR_EMAIL)
        assert b"Points available: 0" in response.data


class TestInsufficientPoints:
    def test_booking_beyond_balance_is_rejected(self, client):
        response = book_places(client, VALID_COMPETITION, POOR_CLUB, "5")

        assert b"Not enough points" in response.data

    def test_rejected_booking_keeps_points_unchanged(self, client):
        book_places(client, VALID_COMPETITION, POOR_CLUB, "5")

        response = login(client, POOR_EMAIL)
        assert b"Points available: 4" in response.data

    def test_rejected_booking_keeps_places_unchanged(self, client):
        book_places(client, VALID_COMPETITION, POOR_CLUB, "5")

        response = login(client, POOR_EMAIL)
        assert b"Number of Places: 25" in response.data
