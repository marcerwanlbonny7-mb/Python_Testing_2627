import pytest

from server import loadClubs, loadCompetitions


class TestDataLoading:
    def test_missing_clubs_file_gives_clear_message(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc:
            loadClubs()

        assert "clubs.json" in str(exc.value)

    def test_corrupt_clubs_file_gives_clear_message(
        self, tmp_path, monkeypatch
    ):
        (tmp_path / "clubs.json").write_text(
            "{not valid json", encoding="utf-8"
        )
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc:
            loadClubs()

        assert "clubs.json" in str(exc.value)
        assert "JSON" in str(exc.value)

    def test_missing_competitions_file_gives_clear_message(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc:
            loadCompetitions()

        assert "competitions.json" in str(exc.value)

    def test_corrupt_competitions_file_gives_clear_message(
        self, tmp_path, monkeypatch
    ):
        (tmp_path / "competitions.json").write_text(
            "definitely not json", encoding="utf-8"
        )
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc:
            loadCompetitions()

        assert "competitions.json" in str(exc.value)
        assert "JSON" in str(exc.value)

    def test_clubs_file_without_key_gives_clear_message(
        self, tmp_path, monkeypatch
    ):
        (tmp_path / "clubs.json").write_text("{}", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc:
            loadClubs()

        assert "clubs" in str(exc.value)

    def test_competitions_file_without_key_gives_clear_message(
        self, tmp_path, monkeypatch
    ):
        (tmp_path / "competitions.json").write_text("{}", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc:
            loadCompetitions()

        assert "competitions" in str(exc.value)
