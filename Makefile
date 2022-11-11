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
	conventional-changelog -p angular -i CHANGELOG.md -s
	@echo -e "\e[32m✔\e[33m Changelog generated. Don't forget to update the version number before committing.\e[0m"
