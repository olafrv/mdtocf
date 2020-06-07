# Markdown To Confluence (mdtocf)

## Requirements

This solutions has been tested and designed for:

* [Ubuntu 18.04 LTS](https://releases.ubuntu.com/)
* [Python 3.7.5](https://docs.python.org/3/) and several python libraries:
  * [PickelDB v0.9](https://pythonhosted.org/pickleDB/)
  * [Mistune v2.0 Markdown Parser](https://mistune.readthedocs.io/en/latest/)
  * [Atlassian Python API v1.5](https://atlassian-python-api.readthedocs.io/)

Please see [requirements.txt](https://github.com/olafrv/mdtocf/blob/master/requirements.txt)
for specific python packages/modules versions required.

## Missing Features (Todo)

* Attachments (e.g. images, pdf, etc.)

# Usage

## Setup python virtual environment

Commands vary depending on the repository and usage options:

* PyPI (Only for Option A below).
* Github (Only for Options B, C and D below).

### Using PyPI Package

```
apt install -y virtualenv python3.7 python-pip
virtualenv --python=python3.7 venv
chmod +x venv/bin/activate
. venv/bin/activate
python -m pip install --upgrade pip
pip install mdtocf
```

### Using Github Repository

```shell
apt install -y virtualenv python3.7 python-pip
git clone "https://github.com/olafrv/mdtocf.git" --branch 1.0.0-rc1 --single-branch
cd mdtocf
virtualenv --python=python3.7 venv
chmod +x venv/bin/activate
. venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
chmod +x run.sh
```

## Source markdown and database directores

An [example markdown directory](https://github.com/olafrv/mdtocf) is shown here:

```shell
find tests/
./tests
./tests/A
./tests/A/aa.md
./tests/A/_index.md
./tests/A/B
./tests/A/B/bb.md
./tests/example.png
./tests/example.md
```

You must create the *dbs* directory before proceeding:
```
mkdir dbs
```

## Option A. Publish using your own python script

Install the package:
```
pip install mdtocf
```

An example based on [mdtocf.py](https://github.com/olafrv/mdtocf/blob/master/md2cf.py):
```python
confluenceUsername = "olafrv@gmail.com"
confluenceApiToken = "****************"
confluenceUrl = "https://olafrv.atlassian.net"
confluenceSpace = "TEST"
confluenceParentPageId = "33114"
confluencePageTitlePrefix = "[Test] "
markdownDir = "./tests"
dbPath = "./dbs/tests.db"

from classes.ConfluencePublisher import ConfluencePublisher
confluencePublisher = ConfluencePublisher(
    url=confluenceUrl,
    username=confluenceUsername,
    apiToken=confluenceApiToken,
    pageTitlePrefix=confluencePageTitlePrefix,
    markdownDir=markdownDir,
    dbPath=dbPath,
    space=confluenceSpace,
    parentPageId=confluenceParentPageId,
    forceUpdate=False,
    forceDelete=False,
    skipUpdate=False
)
#confluencePublisher.delete()
confluencePublisher.publish()
```

### Option B. Publish using local script

```shell
./run.sh \
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "****************" \
    --confluenceUrl "https://olafrv.atlassian.net" \
    --confluenceSpace "TEST" \
    --confluenceParentPageId "33114" \
    --confluencePageTitlePrefix "[Test] " \
    --markdownDir ./tests \
    --db ./dbs/tests.db
```

### Option C. Publish using Docker (Image locally built)

```shell
docker build -t mdtocf .
docker run --rm -it \
    --mount type=bind,source="$(pwd)"/tests,target=/mdtocf/tests \
    --mount type=bind,source="$(pwd)"/dbs,target=/mdtocf/dbs \
    mdtocf \
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "****************" \
    --confluenceUrl "https://olafrv.atlassian.net"   \
    --confluenceSpace "TEST" \
    --confluenceParentPageId "33114" \
    --confluencePageTitlePrefix "[Test] " \
    --markdownDir "./tests" \
    --db "./dbs/tests.db"
```

### Option D. Publish using Docker (Image downloaded from Github's Packages)

```shell
docker run --rm -it \
    --mount type=bind,source="$(pwd)"/tests,target=/mdtocf/tests \
    --mount type=bind,source="$(pwd)"/dbs,target=/mdtocf/dbs \
    docker.pkg.github.com/olafrv/mdtocf/mdtocf:1.0.0-rc1
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "****************" \
    --confluenceUrl "https://olafrv.atlassian.net"   \
    --confluenceSpace "TEST" \
    --confluenceParentPageId "33114" \
    --confluencePageTitlePrefix "[Test] " \
    --markdownDir "./tests" \
    --db "./dbs/tests.db"
```

## Output and Results

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

Rendering and publishing **./tests** produce the following final result in Confluence:

![Result in Confluence](https://raw.githubusercontent.com/olafrv/mdtocf/master/tests/example.png)

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
Attlasian Confluence. A test for this is available in **regexp_test.py**).

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
