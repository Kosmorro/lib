black:
	poetry run black kosmorrolib

.PHONY: tests
tests: doctests

coverage-doctests:
	python3 -m poetry run coverage run tests.py

coverage-report:
	python3 -m poetry run coverage report

doctests:
	python3 -m poetry run python tests.py

changelog:
	npm install conventional-changelog-cli
	./node_modules/.bin/conventional-changelog -p angular -i CHANGELOG.md -s
	rm -rf node_modules package.json package-lock.json
