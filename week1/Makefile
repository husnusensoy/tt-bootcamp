all: data/profiles.jsonl data/profiles.csv data/profiles.txt data/profiles-col

fix:
	uv run isort *.py
	uv run ruff format --line-length 100 --target-version py311 *.py
	uv run ruff check *.py  --fix 
	#uv run mypy *.py


data/profiles.jsonl: 
	@echo Creating sample data
	@mkdir -p data
	@uv run python datagen.py --sample 100000 data/profiles.jsonl


data/profiles.csv: data/profiles.jsonl
	@echo Create csv file
	@uv run python delimiter.py data/profiles.jsonl data/profiles.csv

data/profiles.txt: data/profiles.jsonl
	@echo Create fix length file
	@uv run python fix-length.py data/profiles.jsonl data/profiles.txt

data/profiles-col: data/profiles.jsonl
	@echo Create columnar format
	@uv run python columnar.py data/profiles.jsonl data/profiles-col

clean:
	rm -r data/*
