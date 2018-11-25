import sqlite3

conn = sqlite3.connect('site.db')
conn.execute('CREATE TABLE cards (tel TEXT, mob TEXT,email TEXT,fio TEXT, role TEXT, pos TEXT, org TEXT, soft TEXT, etc TEXT)')
conn.close()
