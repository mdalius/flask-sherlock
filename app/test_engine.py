import json
from pathlib import Path

import pytest

from run import read_data
from rengine import Sherlock


def test_sherlock_recommend_default_lucky_choice(monkeypatch):
    movies = [
        {"title": "Movie A", "genre": ["comedy"], "stars": ["Actor A"], "rating": 5.0},
        {"title": "Movie B", "genre": ["drama"], "stars": ["Actor B"], "rating": 6.0},
    ]
    monkeypatch.setattr("rengine.random.choice", lambda seq: movies[1])

    sherlock = Sherlock(movies, {})
    recommendation = sherlock.recommend()

    assert recommendation == [movies[1]]


def test_sherlock_recommend_matches_genre_and_star():
    movies = [
        {"title": "Kingpin", "genre": ["comedy"], "stars": ["Bill Murray"], "rating": 6.9},
        {"title": "Groundhog Day", "genre": ["comedy"], "stars": ["Bill Murray"], "rating": 8.0},
        {"title": "Lost in Translation", "genre": ["comedy", "drama"], "stars": ["Scarlett Johansson"], "rating": 7.7},
        {"title": "Oppenheimer", "genre": ["drama"], "stars": ["Cillian Murphy"], "rating": 8.4},
    ]

    sherlock = Sherlock(movies, {"title": "Kingpin"})
    recommendation = sherlock.recommend()

    assert [movie["title"] for movie in recommendation] == ["Groundhog Day", "Lost in Translation"]
    assert recommendation[0]["rating"] >= recommendation[1]["rating"]


def test_read_data_returns_error_for_missing_file():
    data, errors = read_data("/tmp/nonexistent-movie-db.json")

    assert data == []
    assert errors == ["Unable to load movie data."]


def test_read_data_returns_error_for_invalid_json(tmp_path):
    bad_file = tmp_path / "invalid.json"
    bad_file.write_text("{ invalid json }")

    data, errors = read_data(str(bad_file))

    assert data == []
    assert errors == ["Unable to load movie data."]
