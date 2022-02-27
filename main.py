import argparse

from src import Config, Db


def main(args: argparse.Namespace):
    config = Config(args.config)
    db = Db(config)
    import csv
    with open("junk/nestest_log_comma.csv", newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            row = list(column.strip() for column in row)
            key = int("0x" + row[0], 16)
            row[0] = key
            db.insert("nestest_log", row)

    print(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MyDB: A database.')
    parser.add_argument('config', metavar='C', type=str, help='a config file')

    args = parser.parse_args()
    main(args)



