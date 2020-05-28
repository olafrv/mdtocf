import argparse
import pickledb

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbpath', help='e.g. ./docs/hashes.db')
    pickledb.load(args.)

if __name__ == "__main__":
   main()