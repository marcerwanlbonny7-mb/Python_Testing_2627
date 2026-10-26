from server import competitions

SPRING = "Spring Festival"
FALL = "Fall Classic"
CLUB = "Simply Lift"
EMAIL = "john@simplylift.co"


def book_places(client, competition, club, places):
    client.post("/showSummary", data={"email": EMAIL})
    return client.post(
        "/purchasePlaces",
        data={"competition": competition, "club": club, "places": places},
        follow_redirects=True,
    )


def login(client, email):
    return client.post(
        "/showSummary", data={"email": email}, follow_redirects=True
    )


def set_places(name, value):
    competition = next(c for c in competitions if c["name"] == name)
    competition["numberOfPlaces"] = str(value)


class TestFullCompetitionMessage:
    def test_full_competition_shows_full_message(self, client):
        set_places(FALL, "0")

        response = book_places(client, FALL, CLUB, "1")

        assert b"This competition is full" in response.data

    def test_full_competition_places_stay_at_zero(self, client):
        set_places(FALL, "0")

        book_places(client, FALL, CLUB, "1")

        response = login(client, EMAIL)
        assert b"Number of Places: 0" in response.data

    def test_welcome_hides_booking_link_when_full(self, client):
        set_places(FALL, "0")

        response = login(client, EMAIL)

        assert b"/book/Fall%20Classic/Simply%20Lift" not in response.data
        assert b"/book/Spring%20Festival/Simply%20Lift" in response.data


class TestConfirmationMessage:
    def test_confirmation_includes_place_count(self, client):
        response = book_places(client, SPRING, CLUB, "3")

        assert b"3 places booked" in response.data

    def test_confirmation_still_reports_success(self, client):
        response = book_places(client, SPRING, CLUB, "3")

        assert b"booking complete" in response.data
