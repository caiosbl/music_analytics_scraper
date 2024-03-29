include .env
export $(shell sed 's/=.*//' .env)

add_artist:
	docker-compose run app python app.py add-artist

update_artist:
	docker-compose run app python app.py update-artist

update_artist_stats:
	docker-compose run app python app.py update-artist-stats

update_all_artists_stats:
	docker-compose run app python app.py update-all-artists-stats

list_artists:
	docker-compose run app python app.py list-artists

compare_artists:
	docker-compose run app python app.py compare-artists

show_youtube_report:
	docker-compose run app python app.py show-youtube-report

show_spotify_report:
	docker-compose run app python app.py show-spotify-report

teardown:
	docker-compose down

clean_cache:
	find . -name "*.cache" -delete
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
