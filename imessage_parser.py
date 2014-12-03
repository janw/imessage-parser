#!/usr/bin/env python

import sqlite3 as sql
from datetime import datetime
from datetime import timedelta

## Settings
here = "Jan"        # Friendly name for "myself"
dbpath = "/Users/janwillhaus/Library/Messages/chat.db"
opponent = ["user@example.com", "+49160123456789"]
there = "Opponent"    # Friendly name for "opponent"

basetime_offset = datetime(2001, 1, 1, 0, 0, 0)
timezone_offset = 1

## DB connection
db = sql.connect(dbpath)
cur = db.cursor()
cur2 = db.cursor()


def main():

    query = ("SELECT ROWID FROM chat WHERE chat_identifier=?")
    wanted_chat_id = list(range(len(opponent)))

    for nn in range(len(opponent)):
        cur.execute(query, (opponent[nn],))

        nextrow = cur.fetchone()
        if nextrow is not None:
            wanted_chat_id[nn] = nextrow[0]
        else:
            wanted_chat_id[nn] = -1

    # Eliminate -1 and be verbose
    wanted_chat_id = [x for x in list if x != -1]
    print("Loading opponent chat IDs:", wanted_chat_id, "...")

    message_id_list = []
    for n in wanted_chat_id:
        query = ("SELECT message_id FROM chat_message_join WHERE chat_id=?")
        cur.execute(query, (n,))
        for p in cur:
            message_id_list.append(p[0])

    query = ("SELECT ROWID,text,date,is_from_me FROM message" +
             " ORDER BY date ASC")
    cur.execute(query)

    for row in cur:
        if row[0] in message_id_list:

            date = basetime_offset + timedelta(timezone_offset, row[2])
            print(date)

            if row[3] is 0:
                print('{0:>10s} said on {1}:  '.format(
                      there,
                      date.strftime("%d.%m.%Y %H:%M:%S")), row[1])
            else:
                print('{0:>10s} said on {1}:  '.format(
                      here,
                      date.strftime("%d.%m.%Y %H:%M:%S")), row[1])


if __name__ == "__main__":
    main()
