iTunes Artwork Finder
=====================

This repository now includes a small Python package which provides a programmatic
way to search the iTunes API for artwork URLs. The original JavaScript and PHP
files are still present for reference.

## Python usage

Install the package in editable mode:

```bash
pip install -e .
```

Then use it in your own code:

```python
from itunes_artwork_finder import search_artwork

results = search_artwork("Ted Lasso", entity="tvSeason", country="us")
for item in results:
    print(item["title"], item["hires"])
```

## Web usage

This is the JavaScript and PHP code that powers the iTunes Artwork Finder available at [https://bendodson.com/projects/itunes-artwork-finder/](https://bendodson.com/projects/itunes-artwork-finder/)

To use on your own site, simply upload both the JavaScript and PHP files and then initialise the script with something like:

	<div>
		<form action="" method="get" accept-charset="utf-8" id="iTunesSearch">
			<select name="entity" id="entity">
				<option value="tvSeason">TV Show</option>
				<option value="movie">Movie</option>
				<option value="ebook">iBook</option>
				<option value="album">Album</option>
				<option value="software">App (iPhone or Universal)</option>
				<option value="iPadSoftware">App (iPad)</option>
				<option value="macSoftware">App (macOS)</option>
				<option value="audiobook">Audiobook</option>
				<option value="podcast">Podcast</option>
				<option value="musicVideo">Music Video (may not work)</option>
				<option value="id">Apple ID (Movie)</option>
				<option value="idAlbum">Apple ID (Album)</option>
				<option value="shortFilm">Short Film</option>
			</select>
			<input type="text" class="text" name="query" id="query" />
			<select name="country" id="country">
				<option value='us'>United States of America</option>
				<option value='gb'>United Kingdom</option>
			</select>
			<input type="submit" class="submit" value="Get the artwork" />
		</form>
	</div>

	<div id="results">

	</div>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="itunes.js"></script>

You will need to amend the first line within `itunes.js` so that the `pathToAPI` variable points to the absolute URL of the `api.php` file running on a PHP server.
