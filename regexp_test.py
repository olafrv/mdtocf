#!/usr/bin/python3.7
import re

file = open('./tests/example.md',mode='r')
content = file.read()
file.close()

# RE of classes/MetadataPlugin.py
p = re.compile((
	r'(?:---)'
	r'((?:\s+)([a-z]+ *:[ \S]+(?:\s+))+)'
	r'(?:---)'
), flags=re.M | re.I )

m = p.match(content)

if m:
    print('Match found:', m.group(1))
else:
    print('No match')

