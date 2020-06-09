# Requirements

This Python package has been tested and designed for:

* [Ubuntu 18.04 LTS](https://releases.ubuntu.com/)
* [Python 3.7.5](https://docs.python.org/3/) and several python libraries:
  * [PickelDB v0.9](https://pythonhosted.org/pickleDB/)
  * [Mistune v2.0 Markdown Parser](https://mistune.readthedocs.io/en/latest/)
  * [Atlassian Python API v1.5](https://atlassian-python-api.readthedocs.io/)

Please see [requirements.txt](https://github.com/olafrv/mdtocf/blob/master/requirements.txt)
for specific python packages/modules versions required.

# Missing Features (Todo)

* Attachments (e.g. images, pdf, etc.)

# Install

Download the package and prepare Python environment alternatives:

```shell
git clone "https://github.com/olafrv/mdtocf.git"
cd mdtocf
make virtualenv
```

Install the package for its use:

**Note:** If you skip virtual environment you should ensure using python >= 3.7

```shell
source venv/bin/activate         # Activate virtual environment (optional)
make install                     # Option 1: Use local package in ./mdtocf
make install-pypi                # Option 2: Install package from PyPI
mkdir -p ~/dbs                   # Create temporal database directory
deactivate                       # Deactivate virtual environment (if activated)
```

See an example code in [mdtocf.py](https://github.com/olafrv/mdtocf/blob/master/mdtocf/mdtocf.py)
and the target *test-publish* inside [Makefile](https://github.com/olafrv/mdtocf/blob/master/mdtocf/Makefile)
show some parameters examples.

# Publish using local script

**Note:** If you skip virtual environment you should ensure using python >= 3.7

```shell
source venv/bin/activate               # Virtual environment (if created)
PYTHON=$(make python-path)             # Used: ven/bin/python or $PATH (python3.7, python3 or python)
${PYTHON} -m mdtocf.mdtocf --help
${PYTHON} -m mdtocf.mdtocf \ 
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "****************" \
    --confluenceUrl "https://olafrv.atlassian.net" \
    --confluenceSpace "TEST" \
    --confluenceParentPageId "33114" \
    --confluencePageTitlePrefix "[Test] " \
    --markdownDir ./examples \
    --db ~/dbs/examples.db
deactivate                             # Deactivate virtual environment (Optional)
```

# Publish using Docker (Image locally built)

```shell
make docker
docker run --rm -it mdtocf --help
docker run --rm -it \
    --mount type=bind,source="$(pwd)"/examples,target=/mdtocf/examples \
    --mount type=bind,source=~/dbs,target=/mdtocf/dbs \
    mdtocf \
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "****************" \
    --confluenceUrl "https://olafrv.atlassian.net"   \
    --confluenceSpace "TEST" \
    --confluenceParentPageId "33114" \
    --confluencePageTitlePrefix "[Test] " \
    --markdownDir "./examples" \
    --db ~/dbs/examples.db
```

# Publish using Docker (Image downloaded from Github's Packages)

```shell
# Check <VERSION> in https://github.com/olafrv/mdtocf/packages 
export IMAGE=docker.pkg.github.com/olafrv/mdtocf/mdtocf:<VERSION> 
docker run --rm -it $IMAGE --help
docker run --rm -it \
    --mount type=bind,source="$(pwd)"/examples,target=/mdtocf/examples \
    --mount type=bind,source=~/dbs,target=/mdtocf/dbs \
    $IMAGE
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "****************" \
    --confluenceUrl "https://olafrv.atlassian.net"   \
    --confluenceSpace "TEST" \
    --confluenceParentPageId "33114" \
    --confluencePageTitlePrefix "[Test] " \
    --markdownDir ./examples \
    --db ~/dbs/examples.db
```

# Output and Results

Output:
```
UPD => Title: [Test] Folder A
Can't find '[Test] Folder A' page on the https://olafrv.atlassian.net/wiki!
IDX => Title: [Test] Folder B
Can't find '[Test] Folder B' page on the https://olafrv.atlassian.net/wiki!
UPD => Title: [Test] 1
Can't find '[Test] 1' page on the https://olafrv.atlassian.net/wiki!
UPD => Title: [Test] Page AA
Can't find '[Test] Page AA' page on the https://olafrv.atlassian.net/wiki!
UPD => Title: [Test] Example Page
Can't find '[Test] Example Page' page on the https://olafrv.atlassian.net/wiki!
```
The *"Can't find..."* means *"not found but creating..."* (Python Atlassian API).

## Results in Confluence

Rendering and publishing **./examples** produce the following final result in Confluence:

![Result in Confluence](https://raw.githubusercontent.com/olafrv/mdtocf/master/examples/example.png)

## About Markdown Compatibility

This scripts depends on [Mistune v2 Markdown Parser](https://mistune.readthedocs.io/en/latest/),
compatible with [CommonMark](https://spec.commonmark.org)

The (optional) metadata heading in markdown (.md) files likes the one which follows below used by [Hugo](https://gohugo.io/getting-started/quick-start/), it is not part of CommonMarkdown standard, but just a popular way of specify in YAML markdown metadata usable for external tools.
```yaml
title: My Page Title
date: 2019-03-26T08:47:11+01:00
draft: true
chapter: true
kind: index
```
It is parsed and partially used by this script to organize the content in
Attlasian Confluence. A test for this can be run:

```shell
make test-re
```

# References

## Markdown

* https://spec.commonmark.org
* https://spec.commonmark.org/dingus/

## Mistune v2

* https://github.com/lepture/mistune
* https://mistune.readthedocs.io/en/latest/

## Python v3

* https://docs.python.org/3/
* https://docs.python.org/3/howto/regex.html
* https://pypi.org/project/atlassian-python-api/
* https://atlassian-python-api.readthedocs.io/confluence.html

## Confluence and Storage Format (Cloud API)

* https://developer.atlassian.com/cloud/confluence/rest/
* https://confluence.atlassian.com/doc/confluence-server-documentation-135922.html
* https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html
* https://confluence.atlassian.com/doc/macros-139387.html
* https://confluence.atlassian.com/conf59/code-block-macro-792499083.html
* https://confluence.atlassian.com/confkb/how-to-get-confluence-page-id-648380445.html
* https://confluence.atlassian.com/doc/delete-or-restore-a-page-139429.html
