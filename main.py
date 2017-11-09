import argparse
import settings

from gurupali_facebook.core import create_tables, crawl_group, analyze

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('command', metavar='c', type=str,
                    help='the command name to execute')
args = parser.parse_args()

if __name__ == '__main__':
    if args.command == 'create-tables':
        create_tables(settings)
    elif args.command == 'crawl-group':
        crawl_group(settings)
    elif args.command == 'analyze':
        analyze(settings)
