help:
	@echo 'Makefile for managing web application                              '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo ' make up               creates containers and starts service       '
	@echo ' make down             stops service and removes containers        '
	@echo '                                                                   '
	@echo ' make migrate          run all migration                           '
	@echo '                                                                   '
	@echo ' make test-up          creates test db and start service           '
	@echo ' make test-down        stops service and removes container         '
	@echo '                                                                   '
	@echo ' make view-docs        view docs page                              '
	@echo '                                                                   '

up:
	docker compose -f docker/docker-compose.yaml up -d --build

down:
	docker compose -f docker/docker-compose.yaml down

migrate:
	cd docker/ && docker compose exec backend alembic upgrade head

test-up:
	docker compose -f docker/docker-compose.tests.yaml up -d --build

test-down:
	docker compose -f docker/docker-compose.tests.yaml down

view-docs:
	open http://localhost:8000/docs/
