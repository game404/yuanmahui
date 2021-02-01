#!/usr/bin/env python

import time
import sqlite3
import os

DB_FILE = "guests.db"

def init_db():
	conn = sqlite3.connect(DB_FILE)
	cursor = conn.cursor()
	# Create table
	cursor.execute('''CREATE TABLE "guests" (
	"id"	INTEGER,
	"ts"	INTEGER,
	PRIMARY KEY("id")
);''')
	# Save (commit) the changes
	conn.commit()
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def update_total(ts):
	conn = sqlite3.connect(DB_FILE)
	cursor = conn.cursor()
	cursor.execute("select count(*) from guests")
	total = cursor.fetchone()[0]
	# Insert a row of data
	cursor.execute(f"INSERT INTO guests(ts) VALUES ({ts})")
	# Save (commit) the changes
	conn.commit()
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	return total + 1

print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print('<title>Hello Word！</title>')
print('</head>')
print('<body>')
print('<h2>Hello Python!</h2>')
if not os.path.exists(DB_FILE):
	init_db()
total = update_total(time.time())
print(f'total guest: {total}!')	
print('</body>')
print('</html>')