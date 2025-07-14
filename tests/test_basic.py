from itunes_artwork_finder import search_artwork

def test_search_movie():
    results = search_artwork("The Matrix", entity="movie", limit=1)
    assert isinstance(results, list)
    assert results
    first = results[0]
    assert "title" in first
    assert "url" in first
    print(first)

def test_search_album():
    results = search_artwork("Abbey Road", entity="album", limit=1)
    print(results[0])

test_search_movie()
test_search_album()
