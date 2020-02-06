run:
	@docker-compose up -d --build aq_container
dev:
	@docker exec -it aq_container bash
build:
	@docker-compose build aq_container
down:
	@docker-compose down -v
status:
	@docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
logs:
	@docker logs aq_container -f