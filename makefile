all:
	@echo "make docker   - Run docker container"
	@echo "make down     - Disable docker container"
	@exit 0

docker:
	docker-compose up -d --build

down:
	docker-compose down