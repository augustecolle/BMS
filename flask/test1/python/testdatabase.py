#!/usr/bin/env python
import sqlite3 as lite
import sys
import time

con = lite.connect('./sqlite/test.db')
with con:
    cur = con.cursor()
    cur.execute("select * from Metingen where Timestamp = (select max(Timestamp) from Metingen)")
    row = cur.fetchone()
if con: con.close()

print(row)
