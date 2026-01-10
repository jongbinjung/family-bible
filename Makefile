.PHONY: \
	help \
	init-db \
	run

## Show this help.
help:
	@awk '/^## .*$$/,/^[~\/\.a-zA-Z_-]+:/' ${MAKEFILE_LIST} | \
	awk '!(NR%2){print $$0p}{p=$$0}' |  \
	awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | \
	sort

## Run the app in local
run:
	uv run streamlit run app.py

#################################################################################
# Concrete targets
#################################################################################

uv.lock:
	@uv lock

data/%.parquet: scripts/init_db.py
	rm data/*.parquet || true
	uv run scripts/init_db.py
