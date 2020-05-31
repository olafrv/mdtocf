# Markdown To Confluence (md2cf)

Tested with: 
* Ubuntu 18.04 LTS w/Python 3.7
* Atlassian Confluence API (Cloud)

## Install and Configure

```
sudo apt install virtualenv
sudo apt install python3.7
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install pygments
pip install mistune==2.0.0a4
pip install atlassian-python-api
```

## Push MD to Confluence 

Help:
```
python md2cf.py -h
```

Example:
```
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

# References

## Mistune v2

* https://github.com/lepture/mistune
* https://mistune.readthedocs.io/en/latest/

## Python Confluence API Wrapper

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
