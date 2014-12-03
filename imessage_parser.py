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

headtext = '\n**{0:s} [{1}]**'

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
    person_last = ""
    for row in cur:

        message, person, date = gather_message(row)

        if date is not None:
            date_today = date.year + date.month + date.day

            if date_last != date_today:
                print("## {0}".format(date.strftime("%d.%m.%Y")), file=f)
                person_last = ""
            date_last = date_today

            if person_last != person:
                print(headtext.format(
                  person,
                      date.strftime("%H:%M:%S")), file=f)
            else:
                print("> ", file=f)
            person_last = person

            if message is not None:
                print(">", message, file=f)

            path_list = gather_images(row[0])
            for path in path_list:
                print("![<Attached Image>]({0})".format(path), file=f)

    f.close()


def gather_message(db_row):

    global message_id_list
    message_id = db_row[0]
    person = db_row[3]

    if person is 0:
        person = there
            else:
        person = here

    if message_id in message_id_list:

        date = basetime_offset + timedelta(timezone_offset, db_row[2])
        message_text = db_row[1]

        if message_text is not None:
            message_text = message_text.replace(u'\ufffc', '')
            message_text = message_text.replace('\n',      '\n> ')

        return message_text, person, date
    else:
        return None, None, None


def gather_images(message_id):

            query = ("SELECT * FROM message_attachment_join" +
                     " WHERE message_id=?")
    cur2.execute(query, (message_id,))
    path_list = []

            for attach in cur2:
                query = ("SELECT filename FROM attachment" +
                     " WHERE ROWID=?")
                cur3.execute(query, (attach[1],))
                path = cur3.fetchone()[0]

                if path is not None:

                    path = ospath.expanduser(path)
                    try:
                        if what(path) in image_formats:
                    path_list.append(path)
                    except FileNotFoundError:
                        continue

    return path_list

if __name__ == "__main__":
    main()
