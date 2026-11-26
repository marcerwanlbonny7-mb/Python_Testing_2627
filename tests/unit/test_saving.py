import pytest

from server import (
    loadBookings, loadClubs, loadCompetitions,
    saveBookings, saveClubs, saveCompetitions
)


class TestDataSaving:
    def test_save_clubs_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data = [{"name": "X Club", "email": "x@y.z", "points": 42}]
        saveClubs(data)
        assert loadClubs() == data

    def test_save_competitions_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data = [{
            "name": "C Cup",
            "date": "2026-12-01 10:00:00",
            "numberOfPlaces": 25
        }]
        saveCompetitions(data)
        assert loadCompetitions() == data

    def test_save_bookings_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data = {("Simply Lift", "Spring Festival"): 7}
        saveBookings(data)
        assert loadBookings() == data

    def test_load_bookings_missing_file_returns_empty(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        assert loadBookings() == {}

    def test_load_bookings_corrupt_file_gives_clear_message(
        self, tmp_path, monkeypatch
    ):
        (tmp_path / "bookings.json").write_text(
            "{not valid json", encoding="utf-8"
        )
        monkeypatch.chdir(tmp_path)
        with pytest.raises(SystemExit) as exc:
            loadBookings()
        assert "bookings.json" in str(exc.value)
