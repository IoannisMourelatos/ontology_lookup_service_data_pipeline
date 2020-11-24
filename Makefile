export APP_IMAGE ?= datapipeline
export APP_TAG ?= dev
export APP_PORT ?= 8000

install-deps:
	pip install -r requirements.txt

build-img:
	docker build -f Dockerfile -t ${APP_IMAGE}:${APP_TAG} .

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down -v

make-migration:
	docker-compose exec server alembic revision -m "$(m)"

migrate:
	docker-compose exec server alembic upgrade head

pipeline-step-tests:
	docker-compose run server pytest -v
