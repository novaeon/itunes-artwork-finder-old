from itunes_artwork_finder import search_artwork


def test_search_movie():
    results = search_artwork("The Matrix", entity="movie", limit=1)
    assert isinstance(results, list)
    assert results
    first = results[0]
    assert "title" in first
    assert "url" in first
