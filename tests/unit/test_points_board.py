class TestPointsPage:
    def test_points_page_accessible_without_login(self, client):
        response = client.get("/points")

        assert response.status_code == 200

    def test_points_page_lists_every_club(self, client):
        response = client.get("/points")

        assert b"Simply Lift" in response.data
        assert b"Iron Temple" in response.data
        assert b"She Lifts" in response.data

    def test_points_page_shows_club_points(self, client):
        response = client.get("/points")

        assert b"13" in response.data
        assert b"4" in response.data
        assert b"12" in response.data

    def test_points_page_sorted_by_points_descending(self, client):
        response = client.get("/points")
        data = response.data

        first = data.index(b"Simply Lift")
        second = data.index(b"She Lifts")
        third = data.index(b"Iron Temple")

        assert first < second < third

    def test_points_page_is_read_only(self, client):
        response = client.post("/points", data={}, follow_redirects=False)

        assert response.status_code == 405

    def test_points_page_has_link_from_home(self, client):
        response = client.get("/")

        assert b'href="/points"' in response.data
