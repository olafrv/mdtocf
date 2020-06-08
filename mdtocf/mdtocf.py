"""mdtocf.py

This script convert markdown pages and publish them to confluence pages

"""
import argparse
from mdtocf.classes.ConfluencePublisher import ConfluencePublisher


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--confluenceUsername',
                        required=True, help='e.g. "example@example.com"')
    parser.add_argument('--confluenceApiToken',
                        required=True, help='e.g. "a87D98AfDsf98dsf7AdsNfaa2"')
    parser.add_argument('--confluenceUrl',
                        required=True, help='e.g. "https://example.jira.com/"')
    parser.add_argument('--confluenceSpace',
                        required=True,
                        help='e.g. ~989819389 (Personal Space), 78712486')
    parser.add_argument('--confluenceParentPageId',
                        required=True,
                        help='e.g. "Page Information: ?pageId=1650458860')
    parser.add_argument('--confluencePageTitlePrefix',
                        required=True, help='e.g. "[MyPrefix] "')
    parser.add_argument('--markdownDir',
                        required=True, help='e.g. "../mydocs"')
    parser.add_argument('--dbPath',
                        required=True, help='e.g. "./dbs/mydocs.db"')
    parser.add_argument('--forceUpdate',
                        required=False, default=0,
                        help='1|0, default=0 (No).' +
                        ' Force page update in Confluence')
    parser.add_argument('--forceDelete',
                        required=False, default=0,
                        help='1|0, default=0 (No). Force page removal' +
                        ' (before update) in Confluence.')
    parser.add_argument('--skipUpdate',
                        required=False, default=0,
                        help='1|0, default=0 (No). Skip page update' +
                        ' in Confluence')
    args = parser.parse_args()

    forceUpdate = int(args.forceUpdate) == 1
    forceDelete = int(args.forceDelete) == 1
    skipUpdate = int(args.skipUpdate) == 1

    confluencePublisher = ConfluencePublisher(
        url=args.confluenceUrl,
        username=args.confluenceUsername,
        apiToken=args.confluenceApiToken,
        pageTitlePrefix=args.confluencePageTitlePrefix,
        markdownDir=args.markdownDir,
        dbPath=args.dbPath,
        space=args.confluenceSpace,
        parentPageId=args.confluenceParentPageId,
        forceUpdate=forceUpdate,
        forceDelete=forceDelete,
        skipUpdate=skipUpdate
    )

    confluencePublisher.delete()
    if not skipUpdate:
        confluencePublisher.publish()


if __name__ == "__main__":
    main()
