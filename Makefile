.PHONY: \
	format \
	help \
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

## Runs the pre-commit tasks against all files, automatically fixing files when it can
format:
	${MAKE} -C ../.. format

## List all available versions of medely-stramlit built in production
list-versions:
	${MAKE} -C ../.. list-versions

uv.lock:
	@uv lock

requirements.txt: uv.lock
	@uv export \
		--format requirements.txt \
		--frozen \
		--no-dev \
		--no-hashes \
		--output-file requirements.txt \
		--quiet
