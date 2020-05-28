# Markdown To Confluence (md2cf)

Tested on: Ubuntu 18.04 LTS

```
sudo apt install virtualenv
sudo apt install python3.7
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install mistune==2.0.0a4
pip install pygments
pip install atlassian-python-api
```


```
python md2cf.py -h
```

# References

# Markdown Parser

* https://mistune.readthedocs.io/en/latest/

## Markdown

* https://github.com/adam-p/markdown-here/wiki/Markdown-Here-Cheatsheet

## Confluence

* https://pypi.org/project/atlassian-python-api/
* https://atlassian-python-api.readthedocs.io/confluence.html
* https://confluence.atlassian.com/doc/confluence-server-documentation-135922.html
* https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html
* https://confluence.atlassian.com/confkb/how-to-get-confluence-page-id-648380445.html
* https://confluence.atlassian.com/doc/macros-139387.html
* https://confluence.atlassian.com/conf59/code-block-macro-792499083.html