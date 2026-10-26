class TestSecretaryJourney:
    def test_secretary_can_book_places_end_to_end(self, client):
        home = client.get("/")
        assert home.status_code == 200
        assert b'href="/points"' in home.data

        summary = client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        assert b"john@simplylift.co" in summary.data
        assert b"Points available: 13" in summary.data

        booking_page = client.get("/book/Spring Festival/Simply Lift")
        assert booking_page.status_code == 200

        confirmation = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "3",
            },
            follow_redirects=True,
        )
        assert b"Great-booking complete! 3 places booked." in confirmation.data

        updated = client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        assert b"Points available: 10" in updated.data
        assert b"Number of Places: 22" in updated.data

    def test_overbooking_is_rejected_and_nothing_changes(self, client):
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        first = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "8",
            },
            follow_redirects=True,
        )
        assert b"Great-booking complete! 8 places booked." in first.data

        second = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "8",
            },
            follow_redirects=True,
        )
        assert b"Cannot book more than 12 places" in second.data

        updated = client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        assert b"Points available: 5" in updated.data
        assert b"Number of Places: 17" in updated.data

    def test_typo_then_good_login_recovers_smoothly(self, client):
        wrong = client.post(
            "/showSummary",
            data={"email": "nobody@example.com"},
            follow_redirects=True,
        )
        assert b"Unknown email, please try again" in wrong.data

        good = client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        assert b"john@simplylift.co" in good.data
        assert b"Points available: 13" in good.data


class TestLeaderboardJourney:
    def test_visitor_sees_public_leaderboard_without_login(self, client):
        home = client.get("/")
        assert b'href="/points"' in home.data

        board = client.get("/points")
        assert board.status_code == 200
        data = board.data
        assert data.index(b"Simply Lift") < data.index(b"She Lifts")
        assert data.index(b"She Lifts") < data.index(b"Iron Temple")
        assert b'href="/"' in data
