import sqlite3
conn = sqlite3.connect('my_boards.db')
c = conn.cursor()

def try_insert(user, uuid):
    global boards
    #c.executescript('drop table boards;')
    #conn.commit()
    sql = 'create table if not exists boards (user text, uuid text)'
    c.execute(sql)
    conn.commit()
    c.execute("insert into boards (user, uuid) values (?,?)",(user, uuid))
   
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())
    print (c.execute("SELECT * FROM boards;"))


    #c.execute()
    #conn.commit()
    #conn.close()

