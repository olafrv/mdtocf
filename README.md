# Markdown To Confluence (md2cf)

## Requirements (Tested)

* [Ubuntu 18.04 LTS](https://releases.ubuntu.com/)
* [Python 3.7.5](https://docs.python.org/3/) and several python libraries:
  * [PickelDB v0.9](https://pythonhosted.org/pickleDB/)
  * [Mistune v2.0 Markdown Parser](https://mistune.readthedocs.io/en/latest/)
  * [Atlassian Python API v1.5](https://atlassian-python-api.readthedocs.io/)

Please see **requirements.txt** for specific python (pip) packages/modules.

## Missing Features (Todo)

* Attachments (e.g. images, pdf, etc.)

## Install and Configure

```
sudo apt install virtualenv
sudo apt install python3.7
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Push MD to Confluence 

Help:
```
source venv/bin/activate
python md2cf.py -h
```

Example:
```
source venv/bin/activate
python md2cf.py \
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "****************"   \
    --confluenceUrl "https://olafrv.atlassian.net"   \
    --confluenceSpace "TEST" \
    --confluenceParentPageId "33114" \
    --confluencePageTitleSuffix "[Test]" \
    --markdownDir ./tests \
    --db ./dbs/tests.db
```

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

![Result in Confluence](https://raw.githubusercontent.com/olafrv/md2cf/master/tests/example.png)

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
