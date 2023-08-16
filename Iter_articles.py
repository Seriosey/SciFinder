import sqlite3 as sl

db = sl.connect('SciFinder_data.db')
c = db.cursor()

c.execute("SELECT rowid, * FROM SciFinder_data")
ids = c.fetchall()
for id in ids:
    print(id[1:])

db.close()

# WHERE methods <> 'None'