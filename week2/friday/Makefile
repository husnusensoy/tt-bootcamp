format:
	uv run sqlfluff fix --dialect duckdb *.sql
	uv run nbqa ruff Dam\ Forecast.ipynb --fix
	uv run nbqa isort Dam\ Forecast.ipynb
	uv run ruff format *.py
	uv run ruff check *.py --fix
	uv run isort *.py

feature: format
	duckdb < dam.sql
	head -5 dam-features.csv
