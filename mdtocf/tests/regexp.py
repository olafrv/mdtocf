import sys
from mdtocf.classes.MetadataPlugin import MetadataPlugin


def main():
    print(sys.argv[1])
    file = open(sys.argv[1], mode='r')
    content = file.read()
    file.close()

    # RE of classes/MetadataPlugin.py
    mdp = MetadataPlugin()
    p = mdp.METADATA_PATTERN

    m = p.match(content)

    if m:
        print('Match found:', m.group(1))
    else:
        print('No match')


if __name__ == "__main__":
    main()
