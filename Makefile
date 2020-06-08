VERSION:=$(shell cat VERSION)
PYTHON=venv/bin/python

# General

help:
	${PYTHON} -m mdtocf.mdtocf --help

virtualenv:
	virtualenv --version >/dev/null || sudo apt install -y virtualenv python3.7 python-pip
	test -d venv/ || virtualenv --python=python3.7 venv && ${PYTHON} -m pip install --upgrade pip

install:
	${PYTHON} -m pip install -r requirements.txt

# Development & Testing

test-publish: dev
    # See README.md about $CONFLUENCE* env variables
	# DO NOT REMOVE @ credentials will be exposed!!!
	@${PYTHON} -m mdtocf.mdtocf \
    --confluenceUsername "${CONFLUENCEUSERNAME}" \
	--confluenceApiToken "${CONFLUENCEAPITOKEN}" \
	--confluenceUrl "https://olafrv.atlassian.net" \
	--confluenceSpace "TEST" \
	--confluenceParentPageId "33114" \
	--confluencePageTitlePrefix "[Test] " \
	--markdownDir ./examples \
	--dbPath ~/dbs/tests.db \
	--forceDelete 1 ;

test-re: dev
	${PYTHON} -m mdtocf.tests.regexp ./examples/example.md

dev: virtualenv install

clean: pypi-clean docker-clean
	rm -rf venv/
	find mdtocf/. -type d -name '__pycache__' -empty -delete
	find mdtocf/. -type f -name '*.pyc' -delete

# Docker Image

test-docker: docker
	# docker run --rm -it --entrypoint /bin/bash mdtocf
	docker run --rm -it mdtocf --help

docker: docker-clean
	# https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
	# Step 0: Build Local Image
	docker build -t mdtocf .

docker-clean:
	docker images | grep mdtocf && docker image rm mdtocf || true

# Github Package

github-package: github-docker
	# Step 4: Publish
	docker push docker.pkg.github.com/olafrv/mdtocf/mdtocf:${VERSION}

test-github-docker:
	# Step 3: Inspect
	docker run --rm -it --entrypoint /bin/bash docker.pkg.github.com/olafrv/mdtocf/mdtocf:${VERSION}

github-docker: docker
	# https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
	# Step 1: Authenticate
	echo ${GH_TOKEN} | docker login docker.pkg.github.com -u olafrv --password-stdin
	# Step 2: Tag
	docker tag mdtocf:latest docker.pkg.github.com/olafrv/mdtocf/mdtocf:${VERSION}

# Python Package Index (PyPI)

pypi-live: pypi-clean pypi
	${PYTHON} -m twine upload --skip-existing --username __token__ --password "${PY_LIVE_TOKEN}" dist/*

pypi-test: pypi-clean pypi
	${PYTHON} -m twine upload --skip-existing --username __token__ --password "${PY_TEST_TOKEN}" --repository testpypi dist/*

pypi: virtualenv
	# https://packaging.python.org/tutorials/packaging-projects/
	${PYTHON} -m pip install --upgrade setuptools wheel
	${PYTHON} -m pip install --upgrade twine
	rm -rf ./dist ./build *.egg-info
	${PYTHON} setup.py sdist bdist_wheel

pypi-clean:
	rm -rf dist/ build/ *.egg-info
