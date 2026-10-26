VALID_CLUB = "Simply Lift"
VALID_COMPETITION = "Spring Festival"
FAKE_NAME = "Nonexistent Thing"


class TestBook:
    def test_valid_club_and_competition_shows_booking_page(self, client):
        response = client.get(f"/book/{VALID_COMPETITION}/{VALID_CLUB}")

        assert response.status_code == 200
        assert b"How many places?" in response.data

    def test_unknown_competition_does_not_crash(self, client):
        response = client.get(f"/book/{FAKE_NAME}/{VALID_CLUB}")

        assert response.status_code in (200, 302)

    def test_unknown_club_does_not_crash(self, client):
        response = client.get(f"/book/{VALID_COMPETITION}/{FAKE_NAME}")

        assert response.status_code in (200, 302)

    def test_unknown_competition_shows_error_message(self, client):
        response = client.get(
            f"/book/{FAKE_NAME}/{VALID_CLUB}", follow_redirects=True
        )

        assert b"Something went wrong" in response.data

    def test_unknown_club_shows_error_message(self, client):
        response = client.get(
            f"/book/{VALID_COMPETITION}/{FAKE_NAME}", follow_redirects=True
        )

        assert b"Something went wrong" in response.data
