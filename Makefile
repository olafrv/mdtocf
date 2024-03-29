# https://makefiletutorial.com/

# Attention: Expanded when defined (:=)
VERSION:=$(shell cat VERSION)
API_JSON:=$(shell printf '{"tag_name": "%s","target_commitish": "master","name": "%s","body": "Release of version %s","draft": false,"prerelease": false}' ${VERSION} ${VERSION} ${VERSION})

# Attention: Expanded when called (=)
PYTHON=$(shell ( \
	test -d venv && echo venv/bin/python ) \
	|| ( ! test -z $$(which python3.7) && echo $$(which python3.7) ) \
	|| ( ! test -z $$(which python3) && echo $$(which python3) ) \
	|| echo python \
	)

# General

help: python-version
	${PYTHON} -m mdtocf.mdtocf --help

install: python-version
	${PYTHON} -m pip install -r requirements.txt

install-pypi: python-version
	${PYTHON} -m pip install mdtocf
	# Until we find a solution for install_requires in setup.py
	${PYTHON} -m pip install -r requirements.txt

uninstall: python-version
	${PYTHON} -m pip uninstall -y -r requirements.txt

virtualenv:
	sudo apt install -y virtualenv python3.7 python3-pip
	test -d venv/ || virtualenv --python=python3.7 venv && venv/bin/python -m pip install --upgrade pip

python-path:
	@echo ${PYTHON}

python-version:
	@echo ${PYTHON}; 
	@${PYTHON} --version 2>&1 | grep "Python 3.7" && exit 0 || ${PYTHON} --version && exit 1

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
	${PYTHON} -m pip install -r requirements-dev.txt

clean: pypi-clean docker-clean
	rm -rf venv/
	find mdtocf/. -type d -name '__pycache__' -empty -delete
	find mdtocf/. -type f -name '*.pyc' -delete

# Github Release

# How to delete tags/releases?
# First, git tag -d 1.0.4
# Second, git push --delete origin 1.0.4
# Finally, https://github.com/olafrv/mdtocf/releases (Discard Danlging Draft)

github-release-delete:

github-release:
    # https://developer.github.com/v3/repos/releases/#create-a-release
	# https://developer.github.com/changes/2020-02-10-deprecating-auth-through-query-param/
	git diff --exit-code
	git diff --cached --exit-code
	git tag -d ${VERSION} && git push --delete origin ${VERSION} || /bin/true
	git tag ${VERSION} && git push origin ${VERSION}
	# DO NOT REMOVE @ credentials will be exposed!!!
	@echo '${API_JSON}' | curl -H 'Authorization: token ${GH_TOKEN}' -d @- https://api.github.com/repos/olafrv/mdtocf/releases

# Docker Image

test-docker: docker
	# docker run --rm -it --entrypoint /bin/bash mdtocf
	docker run --rm -it mdtocf --help

docker: docker-clean
	# https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
	# Step 0: Build Local Image
	docker build -t mdtocf .

docker-clean:
	docker images | grep mdtocf | awk '{print $$1":"$$2}' | sort | xargs --no-run-if-empty -n1 docker image rm

# Github Package

github-package: github-docker
	# Step 4: Publish
	docker push docker.pkg.github.com/olafrv/mdtocf/mdtocf:${VERSION}

test-github-docker: github-docker
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

pypi: python-version
	# https://packaging.python.org/tutorials/packaging-projects/
	${PYTHON} -m pip install --upgrade setuptools wheel
	${PYTHON} -m pip install --upgrade twine
	rm -rf ./dist ./build *.egg-info
	${PYTHON} setup.py sdist bdist_wheel

pypi-clean:
	rm -rf dist/ build/ *.egg-info
