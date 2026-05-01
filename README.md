# BrewSpot

A command-line cafe management system written in Python. It lets you build and maintain a personal collection of cafes — add them manually, search and filter them, or scrape them automatically from [ialoc.ro](https://ialoc.ro/restaurante-bucuresti?tip=cafenea). All data is persisted locally in a JSON file between sessions.

## Project Structure

* `cli/cli.py`: Main CLI loop, menu rendering, and all user interaction.
* `collection/cafe_collection.py`: In-memory collection with add, search, sort, and filter logic.
* `models/cafe.py`: Cafe data model and JSON serialization.
* `scraper/cafe_scraper.py`: Web scraper for ialoc.ro — extracts name, address, rating, price, and benefits.
* `storage/file_manager.py`: JSON persistence layer, handles reading and writing to disk.
* `main.py`: Entry point of the application.


## Features

### 1. Cafe Collection Management (`cafe_collection.py`)

- **Add** a cafe manually or from scraping results — duplicates are rejected based on name + address matching.
- **Search** by name with case-insensitive partial matching.
- **Filter** by minimum rating to surface only high-quality spots.
- **Sort** the entire collection by rating in descending order.
- **Remove** a cafe by name.

### 2. Web Scraping (`cafe_scraper.py`)

- Scrapes the cafe listing from `ialoc.ro` using `requests` and `BeautifulSoup`.
- Extracts: name, address, rating, price tier, and available benefits (WiFi, terrace, pet-friendly, vegan).
- **Price mapping**: translates Romanian keywords (`accesibil`, `moderat`, `premium`, `exclusivist`) into a universal `$` / `$$` / `$$$` / `$$$$` format.
- **Name cleaning**: strips discount percentages and promotional labels (e.g. "Nou pe ialoc") from titles.
- **Deduplication**: removes repeated entries before returning results.

### 3. Data Persistence (`file_manager.py` + `cafe_collection.py`)

- Collection is saved to and loaded from a local `dictionar.json` file.
- Data is automatically saved on exit.
- Handles missing or corrupted JSON files gracefully — starts with an empty collection instead of crashing.

### 4. Interactive CLI (`cli.py`)

The main menu exposes all functionality through a numbered interface:

0) ``Exit``: Saves automatically before quitting.
1) ``Show cafes``: Lists all cafes sorted by rating.
2) ``Add cafe``: Manually input a new cafe.
3) ``Search cafe``: Search by name (partial match supported).
4) ``Scrape cafes``: Fetch from [ialoc.ro](https://ialoc.ro/restaurante-bucuresti?tip=cafenea) and merge into the collection.
5) ``Save``: Write current state to disk.

## Data Model

Each `Cafe` object holds the following fields:

* `name`: Name of the cafe.
* `address`: Street address.
* `price`: Price tier (`$` to `$$$$`).
* `program`: Opening hours.
* `benefits`: List of amenities (e.g. wifi, terasa, pet friendly, vegan).
* `rating`: Score from 0 to 5.

## Installation & Usage

**1. Clone the repository**

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the app:**
```bash
python main.py
```

## Requirements

* `requests`: HTTP requests for scraping.
* `beautifulsoup4`: HTML parsing.
* `colorama`: Colored terminal output.