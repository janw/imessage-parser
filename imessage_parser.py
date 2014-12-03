#!/usr/bin/env python

import sqlite3 as sql
from datetime import datetime
from datetime import timedelta
from imghdr import what
from os import path as ospath

## Settings
here = "Jan"        # Friendly name for "myself"
dbpath = "/Users/janwillhaus/Library/Messages/chat.db"
opponent = ["user@example.com", "+49160123456789"]
there = "Opponent"    # Friendly name for "opponent"
output_file = "conversation.md"

basetime_offset = datetime(2001, 1, 1, 0, 0, 0)
timezone_offset = 1
image_formats = ('png', 'jpeg', 'bmp', 'gif')

headtext = '**{0:s} [{1}]**'

## DB connection
db = sql.connect(dbpath)
cur = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()

message_id_list = []


def main():

    f = open(output_file, 'w')
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
    wanted_chat_id = [x for x in wanted_chat_id if x != -1]
    print("Loading opponent chat IDs:", wanted_chat_id, "...")

    global message_id_list
    for n in wanted_chat_id:
        query = ("SELECT message_id FROM chat_message_join WHERE chat_id=?")
        cur.execute(query, (n,))
        for p in cur:
            message_id_list.append(p[0])

    query = ("SELECT ROWID,text,date,is_from_me FROM message" +
             " ORDER BY date ASC")
    cur.execute(query)

    date_last = 0
    for row in cur:
        if row[0] in message_id_list:

            date = basetime_offset + timedelta(timezone_offset, row[2])
            date_today = date.year + date.month + date.day
            message_text = row[1]

            if message_text is not None:
                # print("!")
                message_text = message_text.replace(u'\ufffc', '')
                message_text = message_text.replace('\n',      '\n> ')

            if date_last != date_today:
                print('##',date.strftime("%d.%m.%Y"),'\n', file=f)
            date_last = date_today

            if row[3] is 0:
                print(headtext.format(
                      there,
                      date.strftime("%H:%M:%S")), file=f)
                print(">", message_text, "\n\n", file=f)
            else:
                print(headtext.format(
                      here,
                      date.strftime("%H:%M:%S")), file=f)
                print(">", message_text, "\n\n", file=f)

            query = ("SELECT * FROM message_attachment_join" +
                     " WHERE message_id=?")
            cur2.execute(query, (row[0],))

            for attach in cur2:
                query = ("SELECT filename FROM attachment" +
                     " WHERE ROWID=?")
                cur3.execute(query, (attach[1],))
                path = cur3.fetchone()[0]

                if path is not None:

                    path = ospath.expanduser(path)
                    try:
                        if what(path) in image_formats:
                            print("![<Attached Image>]({0})".format(path), file=f)
                    except FileNotFoundError:
                        continue
    f.close()

if __name__ == "__main__":
    main()
