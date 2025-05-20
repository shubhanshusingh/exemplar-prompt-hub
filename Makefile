# Makefile

.PHONY: clean build publish tag release

clean:
	rm -rf dist/ build/ *.egg-info/

build: clean
	python -m build

publish: build
	python -m twine upload dist/*
	$(MAKE) tag

tag:
	@version=$$(python setup.py --version); \
	echo "Creating git tag v$$version"; \
	git tag -a "v$$version" -m "Release v$$version"; \
	git push origin "v$$version"

bump-version:
	@echo "Bumping version..."
	@echo "$(NEW_VERSION)" > VERSION
	@echo "Version bumped to $(NEW_VERSION)" 

release:
	@if [ -z "$(NEW_VERSION)" ]; then \
		echo "Error: NEW_VERSION is required. Usage: make release NEW_VERSION=x.y.z"; \
		exit 1; \
	fi
	@echo "Starting release process for version $(NEW_VERSION)..."
	@git diff --quiet || (echo "Error: Uncommitted changes found. Please commit or stash them first." && exit 1)
	@git diff --cached --quiet || (echo "Error: Staged changes found. Please commit them first." && exit 1)
	$(MAKE) bump-version NEW_VERSION=$(NEW_VERSION)
	git add VERSION
	git commit -m "Bump version to $(NEW_VERSION)"
	$(MAKE) publish
	@echo "Release $(NEW_VERSION) completed successfully!" 