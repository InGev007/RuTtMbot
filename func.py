import sqlite3
import time


def createuser(user):
    # 0 - id
    # 1 - first_name
    # 2 - last_name
    # 3 - username
    # 4 - language_code

    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    try:
        res = con.execute(
            'INSERT INTO users (id,first_name,last_name,username,language_code,chat,lastactive) VALUES (%s,"%s","%s","%s","%s",%s,%s);' % (
            user[0], user[1], user[2], user[3], user[4], 0, time.time()))
    except Exception as e:
        res = con.execute('UPDATE users SET chat=0 WHERE id=%s;' % user[0])
    con.commit()
    con.close()
    return


def checkstate(user):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute('SELECT id FROM users WHERE id=%s;' % (user[0]))
    res = res.fetchone()
    if res is None:
        createuser(user)
    res = con.execute('UPDATE users SET lastactive=%s WHERE id=%s;' % (time.time(), user[0]))
    con.commit()
    res = con.execute('SELECT chat FROM users WHERE id=%s;' % user[0])
    res = res.fetchone()
    con.close()
    return res[0]


# def setstate(uid, state):
#     con = sqlite3.connect("./db/bot.db")
#     cur = con.cursor()
#     res = con.execute('UPDATE users SET chat=%s WHERE id=%s;' % (state, uid))
#     res = res.fetchone()
#     con.commit()
#     con.close()
#
#
# def undolearn(uid):
#     con = sqlite3.connect("./db/bot.db")
#     cur = con.cursor()
#     res = con.execute('DELETE FROM t_dial WHERE idu=%s;' % uid)
#     res = con.execute('DELETE FROM tempdict WHERE idu=%s AND ok=0;' % uid)
#     con.commit()
#     res = con.execute('UPDATE tempdict SET good=0, wrong=0 WHERE idu=%s' % uid)
#     con.commit()
#     con.close()
#     return
