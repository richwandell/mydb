from __future__ import annotations
import datetime
import time

from .Db import Db


def save_indexes_thread(db: Db):
    while True:
        now = datetime.datetime.now()
        for key in db.indexes.keys():
            table_indexes = db.indexes[key]
            for col_key in table_indexes.keys():
                for index in table_indexes[col_key]:
                    diff = now - index.last_saved
                    if diff.seconds > 20 and index.updated:
                        index.save()
        time.sleep(10)
