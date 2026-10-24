VALID_EMAIL = "john@simplylift.co"
UNKNOWN_EMAIL = "unknown@example.com"


class TestShowSummary:
    def test_valid_email_displays_club_welcome(self, client):
        response = client.post("/showSummary", data={"email": VALID_EMAIL})

        assert response.status_code == 200
        assert b"Points available" in response.data

    def test_unknown_email_does_not_crash(self, client):
        response = client.post(
            "/showSummary",
            data={"email": UNKNOWN_EMAIL},
            follow_redirects=True,
        )

        assert response.status_code == 200

    def test_unknown_email_displays_error_message(self, client):
        response = client.post(
            "/showSummary",
            data={"email": UNKNOWN_EMAIL},
            follow_redirects=True,
        )

        assert b"Unknown email" in response.data
