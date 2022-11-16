import sqlite3
import os
import updatedb


def checkandupdatedb():
    try:
        con = sqlite3.connect("./db/bot.db")
    except sqlite3.OperationalError:
        os.mkdir('db')
    finally:
        con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res=con.executescript(updatedb.updatesql)
    con.commit()
    con.close()


def dumpdb():
    con = sqlite3.connect("./db/bot.db")
    with open('./db/dump.sql', 'w', encoding='UTF8') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)
    con.close()
