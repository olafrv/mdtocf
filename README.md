# Markdown to Confluence Publisher (mdtocf)

Markdown files/directory publishing to Atlassian Confluence.

## Install from PyPI

```bash
# python3 -m venv venv
# source venv/bin/activate
pip install mdtocf
```

## Publish to Confluence

```bash
python3 -m mdtocf.mdtocf --help
###
# Example usage:
# https://olafrv.atlassian.net/wiki/spaces/~5ed387058884020c24da5a42/pages/131089/Test
# - confluenceUsername: your Atlassian account email.
# - confluenceApiToken: see https://id.atlassian.com/manage-profile/security/api-tokens
# - confluenceUrl: your Atlassian Confluence URL, e.g. https://olafrv.atlassian.net
# - confluenceSpace: the target Confluence space ID, e.g. ~5ed387058884020c24da5a42
# - confluenceParentPageId: the target parent page ID, e.g. 131089
###
python3 -m mdtocf.mdtocf \
    --confluenceUsername "olafrv@gmail.com" \
    --confluenceApiToken "${CONFLUENCE_API_TOKEN}" \
    --confluenceUrl "https://olafrv.atlassian.net" \
    --confluenceSpace "~5ed387058884020c24da5a42" \
    --confluenceParentPageId "131089" \
    --confluencePageTitlePrefix "[Test] " \
    --markdownDir ./examples \
    --db ./examples.db
```

## Console Output

Output:

> **UPD** => Update in Confluence.
> **IDX** => Index page in Confluence.
> **SKP** => Skip update in Confluence.
> **DEL** => Delete page in Confluence.

```bash
# --- Delete ./examples.db file ---
# --- Delete all pages in Confluence space ---
# --- 1st run ---
UPD => Title: [Test] _index.md
IDX => Title: [Test] Folder B
UPD => Title: [Test] bb.md
UPD => Title: [Test] aa.md
UPD Att. => Title: example.png
UPD => Title: [Test] example.md
UPD Att. => Title: example.png
# --- 2nd run (re-run) ---
SKP => Title: [Test] _index.md
SKP => Title: [Test] Folder B
SKP => Title: [Test] bb.md
SKP => Title: [Test] aa.md
DEL Att. => Title: example.png
UPD Att. => Title: example.png
SKP => Title: [Test] example.md
DEL Att. => Title: example.png
UPD Att. => Title: example.png
# --- Delete all sub pages in Confluence space ---
# --- 3nd run ---
SKP => Title: [Test] _index.md
Can't find '[Test] _index.md' page on https://olafrv.atlassian.net/wiki
SKP => Title: [Test] Folder B
Can't find '[Test] Folder B' page on https://olafrv.atlassian.net/wiki
SKP => Title: [Test] bb.md
Can't find '[Test] bb.md' page on https://olafrv.atlassian.net/wiki
SKP => Title: [Test] aa.md
Can't find '[Test] aa.md' page on https://olafrv.atlassian.net/wiki
DEL Att. => Title: example.png
UPD Att. => Title: example.png
SKP => Title: [Test] example.md
Can't find '[Test] example.md' page on https://olafrv.atlassian.net/wiki
DEL Att. => Title: example.png
UPD Att. => Title: example.png
```
The *"Can't find..."* means *"not found but creating..."* (Python Atlassian API).

## Results in Confluence

Rendering and publishing **./examples** produce the following final result in Confluence:

![Result #1](https://raw.githubusercontent.com/olafrv/mdtocf/master/examples/A/example.png)

![Result #2](https://raw.githubusercontent.com/olafrv/mdtocf/master/examples/example.png)

# About Markdown Compatibility

This scripts depends on [Mistune v2 Markdown Parser](https://mistune.readthedocs.io/en/latest/),
compatible with [CommonMark](https://spec.commonmark.org)

The (optional) metadata heading in markdown (.md) files likes the one which 
follows below used by [Hugo](https://gohugo.io/getting-started/quick-start/), 
it is not part of CommonMarkdown standard, but just a popular way of specify 
in YAML markdown metadata usable for external tools.

```yaml
---
title: My Page Title
date: 2019-03-26T08:47:11+01:00
draft: true
chapter: true
kind: index
---
```

It is parsed and partially used by this script to organize the content in
Atlassian Confluence.

# Development

Install from source as local editable package:

```bash
git clone "https://github.com/olafrv/mdtocf.git"
cd mdtocf
python3 -m venv venv
source venv/bin/activate
./release.sh  # development and release to PyPI flow
```

# References

## Python v3

* https://docs.python.org/3/
* https://docs.python.org/3/howto/regex.html
* https://packaging.python.org/tutorials/packaging-projects/
* https://pip.pypa.io/en/stable/reference/pip_install/#git
* https://pip.pypa.io/en/latest/reference/pip_install/#requirements-file-format
* https://packaging.python.org/discussions/install-requires-vs-requirements/

## Markdown Utils

* https://spec.commonmark.org
* https://spec.commonmark.org/dingus/
* https://github.com/lepture/mistune
* https://mistune.readthedocs.io/en/latest/

## Confluence and Storage Format (Cloud API)

* https://pypi.org/project/atlassian-python-api/
* https://atlassian-python-api.readthedocs.io/confluence.html
* https://developer.atlassian.com/cloud/confluence/rest/
* https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html
* https://confluence.atlassian.com/doc/macros-139387.html
* https://confluence.atlassian.com/conf59/code-block-macro-792499083.html
* https://confluence.atlassian.com/confkb/how-to-get-confluence-page-id-648380445.html
* https://confluence.atlassian.com/doc/delete-or-restore-a-page-139429.html
