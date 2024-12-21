# Start the database
start-db:
	docker-compose up -d

# Stop the database
stop-db:
	docker-compose down

# Restart the database
restart-db:
	make stop-db
	make start-db

# Clean up unused Docker containers and volumes
clean:
	docker-compose down --volumes --remove-orphans
