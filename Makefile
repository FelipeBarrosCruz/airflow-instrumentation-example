environment:
	@./scripts/environment

start:
	@docker-compose up -d --build --force-recreate --remove-orphans --wait

restart:
	@docker-compose restart

stop:
	@docker-compose stop

delete:
	@docker-compose down -v
