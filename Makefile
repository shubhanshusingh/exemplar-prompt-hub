# Makefile

.PHONY: clean build publish bump-version

clean:
	rm -rf dist/ build/ *.egg-info/

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

bump-version:
	@echo "Bumping version..."
	@echo "$(NEW_VERSION)" > VERSION
	@echo "Version bumped to $(NEW_VERSION)" 