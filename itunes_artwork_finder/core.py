import requests
from urllib.parse import quote, urlparse

__all__ = ["search_artwork"]

SEARCH_URL = "https://itunes.apple.com/search"
LOOKUP_URL = "https://itunes.apple.com/lookup"


def _build_url(query: str, entity: str, country: str, limit: int) -> str:
    short_film = False
    e = entity
    if entity == "shortFilm":
        short_film = True
        e = "movie"
    if entity in {"id", "idAlbum"}:
        return f"{LOOKUP_URL}?id={quote(query)}&country={country}"
    url = f"{SEARCH_URL}?term={quote(query)}&country={country}&entity={e}&limit={limit}"
    if short_film:
        url += "&attribute=shortFilmTerm"
    return url


def _process_result(result: dict, entity: str) -> dict | None:
    if entity == "id" and result.get("kind") != "feature-movie" and result.get("wrapperType") != "collection":
        return None
    if entity == "idAlbum" and result.get("collectionType") != "Album":
        return None

    width = height = 600
    artwork_url = result.get("artworkUrl100")
    if not artwork_url:
        return None

    data = {}
    data["url"] = artwork_url.replace("100x100", "600x600")

    hires = artwork_url.replace("100x100bb", "100000x100000-999")
    parts = urlparse(hires)
    hires = f"https://is5-ssl.mzstatic.com{parts.path}"

    data["hires"] = hires

    title = result.get("collectionName")
    if entity in {"movie", "id", "shortFilm"}:
        title = result.get("trackName") or result.get("collectionName")
        width = 400
    elif entity == "musicVideo":
        title = f"{result.get('trackName')} (by {result.get('artistName')})"
        width = 640
        height = 464
        data["url"] = hires
    elif entity == "ebook":
        title = f"{result.get('trackName')} (by {result.get('artistName')})"
        width = 400
    elif entity in {"album", "idAlbum"}:
        title = f"{result.get('collectionName')} (by {result.get('artistName')})"
    elif entity == "audiobook":
        title = f"{result.get('collectionName')} (by {result.get('artistName')})"
    elif entity == "podcast":
        title = f"{result.get('collectionName')} (by {result.get('artistName')})"
    elif entity in {"software", "iPadSoftware", "macSoftware"}:
        data["url"] = artwork_url.replace("512x512bb", "1024x1024bb")
        data["appstore"] = result.get("trackViewUrl")
        title = result.get("trackName")
        width = height = 512
    elif entity == "tvSeason":
        title = result.get("collectionName")
    else:
        title = result.get("collectionName")

    if entity in {"album", "idAlbum"} and hires:
        parts = hires.split("/image/thumb/")
        if len(parts) == 2:
            sub = parts[1].split("/")
            sub.pop()
            data["uncompressed"] = f"https://a5.mzstatic.com/us/r1000/0/{'/'.join(sub)}"

    if not title:
        return None
    data["title"] = title
    data["width"] = width
    data["height"] = height
    return data


def search_artwork(query: str, entity: str = "tvSeason", country: str = "us", limit: int = 25) -> list[dict]:
    """Search iTunes for artwork and return processed results."""
    url = _build_url(query, entity, country, limit)
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()

    results = []
    for result in json_data.get("results", []):
        item = _process_result(result, entity)
        if item:
            results.append(item)
    return results
