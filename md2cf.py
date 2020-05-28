import argparse
from classes.ConfluenceRenderer import ConfluenceRenderer
from classes.ConfluencePublisher import ConfluencePublisher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--confluenceUsername', help='e.g. "example@example.com"')
    parser.add_argument('--confluenceApiToken', help='e.g. "a87d98afdsf98dsf7adsnfaa2"')
    parser.add_argument('--confluenceUrl', help='e.g. "https://example.jira.com/"')
    parser.add_argument('--confluenceSpace', help='e.g. ~989819389 (Personal Space), 78712486')
    parser.add_argument('--confluenceParentPageId', help='e.g. "Page Information: ?pageId=1650458860')
    parser.add_argument('--confluencePageTitleSuffix', help='e.g. "[MySuffix]"')
    parser.add_argument('--markdownDir', help='e.g. ./docs/markdown')
    args = parser.parse_args()

    confluencePublisher = ConfluencePublisher(
        args.confluenceUrl,
        args.confluenceUsername,
        args.confluenceApiToken,
        args.markdownDir,
        args.confluenceSpace,
        args.confluenceParentPageId)

    confluencePublisher.delete()
    confluencePublisher.publish()

if __name__ == "__main__":
   main()