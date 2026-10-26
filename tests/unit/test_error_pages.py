import server


class TestErrorPages:
    def test_unknown_url_shows_custom_404(self, client):
        response = client.get("/definitely-not-a-page")

        assert response.status_code == 404
        assert b"Page not found" in response.data

    def test_404_page_links_back_home(self, client):
        response = client.get("/definitely-not-a-page")

        assert b'href="/"' in response.data

    def test_internal_error_shows_custom_500(self, client, monkeypatch):
        def boom():
            raise RuntimeError("test error")

        monkeypatch.setitem(server.app.view_functions, "index", boom)
        monkeypatch.setitem(server.app.config, "TESTING", False)
        monkeypatch.setitem(server.app.config, "PROPAGATE_EXCEPTIONS", False)

        response = client.get("/")

        assert response.status_code == 500
        assert b"internal error" in response.data.lower()


class TestMissingFormFields:
    def test_show_summary_without_email_field_does_not_crash(self, client):
        response = client.post("/showSummary", data={}, follow_redirects=True)

        assert response.status_code == 200
        assert b"Unknown email" in response.data

    def test_purchase_without_competition_field_does_not_crash(self, client):
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        response = client.post(
            "/purchasePlaces",
            data={"club": "Simply Lift", "places": "1"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Something went wrong" in response.data

    def test_purchase_without_club_field_does_not_crash(self, client):
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        response = client.post(
            "/purchasePlaces",
            data={"competition": "Spring Festival", "places": "1"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert response.status_code != 500

    def test_purchase_without_places_field_does_not_crash(self, client):
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        response = client.post(
            "/purchasePlaces",
            data={"competition": "Spring Festival", "club": "Simply Lift"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Invalid number of places" in response.data
