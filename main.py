import argparse

from src import Config, Db


def main(args: argparse.Namespace):
    config = Config(args.config)
    db = Db(config)
    db.save_table_definitions()
    print(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MyDB: A database.')
    parser.add_argument('config', metavar='C', type=str, help='a config file')

    args = parser.parse_args()
    main(args)



