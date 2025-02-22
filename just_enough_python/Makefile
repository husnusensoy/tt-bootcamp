fix:
	@echo Formatting and sanity check...
	@uv run isort *.py
	@uv run ruff format *.py
	@uv run  ruff check *.py --fix

test: fix
	@echo Running tests...
	@uv run pytest *.py
