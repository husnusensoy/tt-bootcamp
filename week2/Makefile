# IMDb dataset base URL
IMDB_BASE_URL=https://datasets.imdbws.com

# Target directory
IMDB_DIR=imdb

# List of IMDb datasets to download
FILES = \
    name.basics.tsv.gz \
    title.akas.tsv.gz \
    title.basics.tsv.gz \
    title.crew.tsv.gz \
    title.episode.tsv.gz \
    title.principals.tsv.gz \
    title.ratings.tsv.gz

# Ensure the target directory exists
$(IMDB_DIR):
	mkdir -p $(IMDB_DIR)

# Download each file into the imdb/ directory
$(IMDB_DIR)/%.tsv.gz: | $(IMDB_DIR)
	curl -o $@ $(IMDB_BASE_URL)/$(notdir $@)

# Target to download all files
all: $(FILES:%=$(IMDB_DIR)/%)

# Clean up downloaded files
clean:
	rm -rf $(IMDB_DIR)

