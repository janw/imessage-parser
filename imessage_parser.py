#!/usr/bin/env python

import sqlite3 as sql
from datetime import datetime
from datetime import timedelta
from imghdr import what
from os import path as ospath

## Settings ###########################
my_name         = "Jan"
dbpath          = "~/Library/Messages/chat.db"
opponent        = ["imessage@example.com", "+49160123456789"]
opponent_name   = "Opponent"
output_file     = "conversation.md"
#######################################

# Some constants
basetime_offset = datetime(2000, 12, 31, 0, 0, 0)
timezone_offset = 1
image_formats = ('png', 'jpeg', 'bmp', 'gif')
headtext = '\n**{0:s} [{1}]**'

# DB connection
db = sql.connect(ospath.expanduser(dbpath))
cur = db.cursor()
cur2 = db.cursor()

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

    placeholder = '?'
    placeholders = ', '.join(placeholder for unused in wanted_chat_id)

    query = ("SELECT message.ROWID, message.text, date, is_from_me FROM message LEFT JOIN chat_message_join ON message.ROWID = chat_message_join.message_id  WHERE chat_id IN (%s)" % placeholders)
    cur.execute(query, wanted_chat_id)

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
        person = opponent_name
    else:
        person = my_name

    date = basetime_offset + timedelta(timezone_offset, db_row[2])
    message_text = db_row[1]

    if message_text is not None:
        message_text = message_text.replace(u'\ufffc', '')
        message_text = message_text.replace('\n', '\n> ')

        return message_text, person, date
    else:
        return None, None, None


def gather_images(message_id):

    query = ("SELECT filename FROM attachment LEFT JOIN message_attachment_join ON attachment.ROWID = message_attachment_join.attachment_id WHERE message_id=?")

    cur2.execute(query, (message_id,))

    path_list = []
    for attachment in cur2:
        if attachment[0] is not None:
            attachment = ospath.expanduser(attachment[0])
            try:
                if what(attachment) in image_formats:
                    path_list.append(attachment)
            except FileNotFoundError:
                continue

    return path_list

if __name__ == "__main__":
    main()
