# Music Analytics Scraper
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains code and documentation for scraping music statistics from various sources.

## Table of Contents
- [Introduction](#introduction)
- [Build](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Music Analytics Scraper project aims to collect and analyze music statistics from different platforms and sources. By scraping data from popular music streaming services, social media platforms, and other sources, we can gain insights into music trends, popularity, and user preferences.

## Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)


## Usage
To usage this repository, you need to have:
- Spotify API key, you can get [here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- Youtube Data API key, you can get [here](https://developers.google.com/youtube/v3/getting-started?hl=pt-br)

With, these keys:

- Copy .env.example file and rename it to .env
- Replace the following values of the variables with your keys

```bash
SPOTIFY_API_CLIENT_ID=your_spotify_client_id
SPOTIFY_API_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
```

## Output
The result output will be saved in a PostgreSQL database, you can access the database using the following credentials (default) (Please see the [docker-compose.yml](docker-compose.yml) file):


```bash
host: localhost
user: postgres
password: mypassword
database: music_analytics
```

## Data content

Current data content:
- Artist
- Album
- Track
- Artist Statistics

From the following sources:
- Spotify
- Youtube

Example of running:

## Adding Artist:
```bash
make add_artist
```

## Updating Artist ids:
```bash
make update_artist
```

## Updating Artist Statistics:
```bash
make update_artist_stats
```

## Updating All Artists Statistics:
```bash
make update_all_artists_stats
```

## Skipping platforms:

Spotify:
```bash
make update_all_artists_stats --skip-spotify
```

Youtube:
```bash
make update_all_artists_stats --skip-youtube
```

## Contributing
Contributions are welcome! Please feel free to submit a [Pull Request](https://github.com/caiosbl/music_analytics_scraper/compare).


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
