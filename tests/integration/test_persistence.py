import json
from pathlib import Path


class TestDataPersistence:
    def _login_and_book_one_place(self, client):
        client.post(
            '/showSummary', data={'email': 'john@simplylift.co'}
        )
        return client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '1',
        })

    def _read_clubs_from_disk(self):
        raw = json.loads(
            Path('clubs.json').read_text(encoding='utf-8')
        )
        return raw['clubs']

    def test_purchase_writes_points_to_disk(self, client):
        before = int(next(
            c for c in self._read_clubs_from_disk()
            if c['name'] == 'Simply Lift'
        )['points'])

        response = self._login_and_book_one_place(client)
        assert response.status_code == 200

        after = int(next(
            c for c in self._read_clubs_from_disk()
            if c['name'] == 'Simply Lift'
        )['points'])
        assert after == before - 1

    def test_purchase_writes_places_to_disk(self, client):
        before = next(
            c for c in json.loads(
                Path('competitions.json').read_text(encoding='utf-8')
            )['competitions'] if c['name'] == 'Spring Festival'
        )['numberOfPlaces']

        response = self._login_and_book_one_place(client)
        assert response.status_code == 200

        after = next(
            c for c in json.loads(
                Path('competitions.json').read_text(encoding='utf-8')
            )['competitions'] if c['name'] == 'Spring Festival'
        )['numberOfPlaces']
        assert int(after) == int(before) - 1

    def test_purchase_writes_bookings_to_disk(self, client):
        response = self._login_and_book_one_place(client)
        assert response.status_code == 200

        bookings_raw = json.loads(
            Path('bookings.json').read_text(encoding='utf-8')
        )
        assert bookings_raw['Simply Lift']['Spring Festival'] == 1
