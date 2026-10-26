from locust import HttpUser, task, between


class GudlftUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post(
            "/showSummary",
            data={"email": "john@simplylift.co"},
            name="POST /showSummary (login)",
        )

    @task(5)
    def load_portal(self):
        self.client.get("/", name="GET / (load)")

    @task(3)
    def load_leaderboard(self):
        self.client.get("/points", name="GET /points (load)")

    @task(2)
    def load_booking_page(self):
        self.client.get(
            "/book/Spring Festival/Simply Lift",
            name="GET /book (load)",
        )

    @task(1)
    def update_booking(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "1",
            },
            name="POST /purchasePlaces (update)",
        )
