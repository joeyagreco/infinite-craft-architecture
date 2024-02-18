# INSTALL DEPENDENCIES
.PHONY: deps
deps:
	@brew install postgresql
	@python3.10 -m pip install -r requirements.dev.txt
	@python3.10 -m pip install -r requirements.txt

# FORMAT PYTHON CODE
.PHONY: fmt
fmt:
	@black --config=pyproject.toml .
	@autoflake --config=pyproject.toml .
	@isort .

# MIGRATE DATABASE TO LATEST
.PHONY: migrate
migrate:
	@alembic upgrade head

# CREATE NEW MIGRATION
.PHONY: new-migration
new-migration:
	@alembic revision -m ${REVISION}

# RUN DOCKER 
.PHONY: up-docker
up-docker:
	@docker-compose up -d

# RESET DB LOCALLY
.PHONY: reset
reset:
# Stop all containers and remove them, along with their volumes
	@docker-compose down -v
# Explicitly remove postgres volume if it exists to ensure data is wiped
	-@docker volume rm infinite-backend_postgres_data 2> /dev/null || true

.PHONY: up
up: up-docker
	@python3.10 main.py



