.DEFAULT_GOAL := build


run:
	docker-compose up --build

rund:
	docker-compose up --build -d

migrate:
	docker-compose run --rm app ./manage.py makemigrations && \
	docker-compose run --rm app ./manage.py migrate

createsuperuser:
	docker-compose run --rm app ./manage.py createsuperuser

prospector:
	docker-compose run --rm app prospector

isort:
	docker-compose run --rm app isort -l120 -m3 --tc $(if $(ISORT_PATH),$(ISORT_PATH), .)

test:
	docker-compose run --rm app pytest --cov

