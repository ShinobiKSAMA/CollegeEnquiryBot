from flask_mysqldb import MySQL
import hashlib

def hashpass(psw):
    hashed_pass = hashlib.md5(psw.encode())
    return hashed_pass.hexdigest()

def delUser(email ,mysql):
    sql = 'DELETE FROM users WHERE email=%s'
    sql2 = 'DELETE FROM chat WHERE usr=%s'
    usr = getUser(email, mysql)
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, (email,))
        mysql.connection.commit()
    except Exception as e:
        print("1st Error"+e)
        return (0,)
    try:
        cur.execute(sql2, (usr,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        return (1,)

def getUser(email, mysql):
    sql = 'SELECT fname FROM users WHERE email=%s'
    cur = mysql.connection.cursor()
    cur.execute(sql, (email,))
    res = cur.fetchone()
    cur.close()

    return res

def getUsers(mysql):
    sql = 'SELECT fname, email FROM users'
    cur = mysql.connection.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()

    return res

def getChat(usr, mysql):
    sql = 'SELECT msg, who FROM chat WHERE usr = %s'
    cur = mysql.connection.cursor()
    cur.execute(sql, (usr,))
    res = cur.fetchall()
    cur.close()

    return res

def add_msg(msg, usr, who, mysql):
    sql2 = "INSERT INTO chat(usr, msg, who) VALUES (%s, %s, %s)"
    cur2 = mysql.connection.cursor()
    try:
        cur2.execute(sql2, (usr, msg, who))
        mysql.connection.commit()
    except Exception as e:
        print(e)
    finally:
        cur2.close()

def login(email, psw, mysql):
    sql = 'SELECT * FROM users WHERE email = %s AND pass = %s'
    cur = mysql.connection.cursor()
    cur.execute(sql, (email, hashpass(psw)))
    res = cur.fetchone()
    cur.close()

    return res

def login_adm(adm, psw, mysql):
    sql = 'SELECT * FROM admin WHERE adm = %s AND pass = %s'
    cur = mysql.connection.cursor()
    print(hashpass(psw))
    cur.execute(sql, (adm, hashpass(psw)))
    res = cur.fetchone()
    cur.close()

    return res

def register(fname, email, psw, mysql):
    sql1 = "SELECT * FROM users WHERE email = %s"
    cur1 = mysql.connection.cursor()
    cur1.execute(sql1, (email,))
    res = cur1.fetchone()
    print(res)
    if res == None:
        sql2 = "INSERT INTO users(fname, email, pass) VALUES (%s, %s, %s)"
        cur2 = mysql.connection.cursor()
        try:
            cur2.execute(sql2, (fname, email, hashpass(psw)))
            mysql.connection.commit()
        except Exception as e:
            return e
        finally:
            cur2.close()
        return "User Registered Successfully"
    else:
        return "User Already Exists"