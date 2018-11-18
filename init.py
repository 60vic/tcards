import sqlite3

conn = sqlite3.connect('site.db')
conn.execute('CREATE TABLE cards (tel TEXT, mob TEXT, fio TEXT, role TEXT, pos TEXT, org TEXT, org_ TEXT, soft TEXT)')
conn.close()
