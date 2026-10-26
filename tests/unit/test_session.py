from server import clubs, competitions

SPRING = "Spring Festival"
CLUB = "Simply Lift"
OTHER_CLUB = "She Lifts"
EMAIL = "john@simplylift.co"


def login(client, email):
    return client.post(
        "/showSummary", data={"email": email}, follow_redirects=True
    )


def book(client, competition, club, places):
    return client.post(
        "/purchasePlaces",
        data={"competition": competition, "club": club, "places": places},
        follow_redirects=True,
    )


class TestLoginRequired:
    def test_booking_page_requires_login(self, client):
        response = client.get(
            f"/book/{SPRING}/{CLUB}", follow_redirects=True
        )

        assert b"Please log in" in response.data

    def test_purchase_requires_login(self, client):
        response = book(client, SPRING, CLUB, "1")

        assert b"Please log in" in response.data

    def test_purchase_without_login_changes_nothing(self, client):
        book(client, SPRING, CLUB, "1")

        response = login(client, EMAIL)
        assert b"Number of Places: 25" in response.data
        assert b"Points available: 13" in response.data


class TestCannotBookForOtherClub:
    def test_purchase_for_other_club_is_rejected(self, client):
        login(client, EMAIL)

        response = book(client, SPRING, OTHER_CLUB, "1")

        assert b"only make bookings for your own club" in response.data

    def test_other_club_is_untouched(self, client):
        she_lifts = next(c for c in clubs if c["name"] == OTHER_CLUB)
        competition = next(
            c for c in competitions if c["name"] == SPRING
        )
        points_before = she_lifts["points"]
        places_before = competition["numberOfPlaces"]

        login(client, EMAIL)
        book(client, SPRING, OTHER_CLUB, "1")

        assert she_lifts["points"] == points_before
        assert competition["numberOfPlaces"] == places_before

    def test_booking_page_of_other_club_is_rejected(self, client):
        login(client, EMAIL)

        response = client.get(
            f"/book/{SPRING}/{OTHER_CLUB}", follow_redirects=True
        )

        assert b"only make bookings for your own club" in response.data


class TestBookForOwnClub:
    def test_logged_in_club_can_book_for_itself(self, client):
        login(client, EMAIL)

        response = book(client, SPRING, CLUB, "2")

        assert b"booking complete" in response.data


class TestLogout:
    def test_logout_forgets_the_club(self, client):
        login(client, EMAIL)
        client.get("/logout")

        response = client.get(
            f"/book/{SPRING}/{CLUB}", follow_redirects=True
        )

        assert b"Please log in" in response.data
