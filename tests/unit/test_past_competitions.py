from datetime import datetime, timedelta

from server import competitions

SPRING = "Spring Festival"
FALL = "Fall Classic"
CLUB = "Simply Lift"
EMAIL = "john@simplylift.co"


def set_date(name, value):
    competition = next(c for c in competitions if c["name"] == name)
    competition["date"] = value


def past_date():
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")


def future_date():
    return (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")


def login(client, email):
    return client.post(
        "/showSummary", data={"email": email}, follow_redirects=True
    )


def book_places(client, competition, club, places):
    client.post("/showSummary", data={"email": EMAIL})
    return client.post(
        "/purchasePlaces",
        data={"competition": competition, "club": club, "places": places},
        follow_redirects=True,
    )


class TestPastCompetitionNotListed:
    def test_past_competition_hidden_from_welcome(self, client):
        set_date(SPRING, past_date())

        response = login(client, EMAIL)

        assert b"Spring Festival" not in response.data

    def test_future_competition_still_listed(self, client):
        set_date(SPRING, future_date())

        response = login(client, EMAIL)

        assert b"Spring Festival" in response.data

    def test_past_competition_hidden_but_other_one_shown(self, client):
        set_date(SPRING, past_date())
        set_date(FALL, future_date())

        response = login(client, EMAIL)

        assert SPRING.encode() not in response.data
        assert FALL.encode() in response.data


class TestPastCompetitionNotBookable:
    def test_booking_page_rejects_past_competition(self, client):
        set_date(SPRING, past_date())
        login(client, EMAIL)

        response = client.get(
            f"/book/{SPRING}/{CLUB}", follow_redirects=True
        )

        assert response.status_code == 200
        assert b"already taken place" in response.data

    def test_purchase_rejects_past_competition(self, client):
        set_date(SPRING, past_date())

        response = book_places(client, SPRING, CLUB, "1")

        assert b"already taken place" in response.data

    def test_rejected_booking_keeps_places_unchanged(self, client):
        set_date(SPRING, past_date())

        book_places(client, SPRING, CLUB, "1")

        competition = next(
            c for c in competitions if c["name"] == SPRING
        )
        assert competition["numberOfPlaces"] == "25"
