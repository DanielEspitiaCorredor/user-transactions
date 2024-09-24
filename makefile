# we want bash behaviour in all shell invocations
SHELL := bash

help: # Show this help
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help               Show this help"
	@echo "  generate-csv       Generate csv with account data"


generate-csv:
	poetry run python3 \
	./user_transactions/scripts/generate_data.py
