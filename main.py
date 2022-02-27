import argparse
from threading import Thread

from src import Config, Db
from src.db.DbIndex import convert_key


def main(args: argparse.Namespace):
    from src.db.save_indexes_thread import save_indexes_thread

    config = Config(args.config)
    db = Db(config)

    t = Thread(target=save_indexes_thread, args=(db,))
    t.daemon = True
    t.start()

    # db.truncate_table("nestest_log")
    # import csv
    # with open("junk/nestest_log_comma.csv", newline='\n') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     for row in spamreader:
    #         row = list(column.strip() for column in row)
    #         # row[0] = convert_key(row[0])
    #         db.insert("nestest_log", row)

    row = db.get_row("nestest_log", 1)
    rows = db.get_rows("nestest_log", [0, 2, 3])

    import time

    def current_milli_time():
        return time.time()

    start = current_milli_time()
    rows = db.find_row("nestest_log", "instruction", "FAEF")
    total = current_milli_time() - start
    print(total)

    start = current_milli_time()
    rows = db.find_row("nestest_log", "instruction", "FAEF", False)
    total = current_milli_time() - start
    print(total)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MyDB: A database.')
    parser.add_argument('config', metavar='C', type=str, help='a config file')

    args = parser.parse_args()
    main(args)



