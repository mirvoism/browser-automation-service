# AI Browser Automation - Development Commands
.PHONY: help build run-gemini run-macstudio run-production dev clean test

# Default target
help:
	@echo "Available commands:"
	@echo "  build          - Build Docker image"
	@echo "  run-gemini     - Run Google Gemini version"
	@echo "  run-macstudio  - Run Mac Studio version"
	@echo "  run-production - Run production visual agent"
	@echo "  dev            - Start development environment"
	@echo "  logs           - Show container logs"
	@echo "  clean          - Clean up containers and images"
	@echo "  test           - Run tests"
	@echo "  setup          - Initial setup (local environment)"

# Docker commands
build:
	docker-compose build

run-gemini:
	docker-compose up browser-automation-gemini

run-macstudio:
	docker-compose up browser-automation-macstudio

run-production:
	docker-compose up production-agent

dev:
	docker-compose up dev-environment

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --rmi local
	docker system prune -f

# Local development commands
setup:
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt -r requirements-macstudio.txt
	playwright install

test:
	python -m pytest tests/ -v

# Quick test commands
test-gemini:
	python examples/google_search.py

test-macstudio:
	python examples/google_search_macstudio.py

test-connection:
	python llm_speed_test.py
