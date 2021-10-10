black:
	pipenv run black kosmorrolib setup.py

.PHONY: tests
tests: doctests

coverage-doctests:
	pipenv run python3 -m coverage run tests.py

coverage-report:
	pipenv run python3 -m coverage report

doctests:
	pipenv run python3 tests.py

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

env:
	@if [[ "$$RELEASE_NUMBER" == "" ]]; \
		then echo "Missing environment variable: RELEASE_NUMBER."; \
		echo 'Example: export RELEASE_NUMBER="1.0.0" (without the leading "v")'; \
		exit 1; \
	fi

changelog:
	conventional-changelog -p angular -i CHANGELOG.md -s
	@echo -e "\e[32m✔\e[33m Changelog generated. Don't forget to update the version number before committing.\e[0m"
	@echo -e "  When everything is good, finish the release with 'make tag'."

tag: env
	git add CHANGELOG.md kosmorrolib/__version__.py
	git commit -m "build: bump version $$RELEASE_NUMBER"
	git tag "v$$RELEASE_NUMBER"
	git checkout features
	git merge main
	git checkout main

	@echo
	@echo -e "\e[1mVersion \e[36m$$RELEASE_NUMBER\e[39m successfully tagged!"
	@echo -e "Invoke \e[33mgit push origin master features v$$RELEASE_NUMBER\e[39m to finish."
