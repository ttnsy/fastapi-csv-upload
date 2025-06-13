.PHONY: test clean retest

test:
	DB_PATH=test.db uv run pytest -s

clean:
	rm -f test.db

retest: clean test
