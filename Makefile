include .env
export $(shell sed 's/=.*//' .env)

run_spotify:
	docker-compose run app python app.py -spotify_artist_id $(id)

run_youtube:
	docker-compose run app python app.py -youtube_artist_id $(id)

teardown:
	docker-compose down

clean_cache:
	find . -name "*.cache" -delete
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
