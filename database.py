import pymysql

user="root"
password="Mk#54421"
database="resume_screening"
port=3306

def select(q):
    con=pymysql.connect(user=user,password=password,host="localhost",database=database,port=port)
    cur=con.cursor(pymysql.cursors.DictCursor)  # FIXED
    cur.execute(q)
    result=cur.fetchall()
    cur.close()
    con.close()
    return result

def insert(q):
    con=pymysql.connect(user=user,password=password,host="localhost",database=database,port=port)
    cur=con.cursor(pymysql.cursors.DictCursor)  # FIXED
    cur.execute(q)
    con.commit()
    result=cur.lastrowid
    cur.close()
    con.close()
    return result

def update(q):
    con=pymysql.connect(user=user,password=password,host="localhost",database=database,port=port)
    cur=con.cursor(pymysql.cursors.DictCursor)  # FIXED
    cur.execute(q)
    con.commit()
    result=cur.rowcount
    cur.close()
    con.close()

def delete(q):
    con=pymysql.connect(user=user,password=password,host="localhost",database=database,port=port)
    cur=con.cursor(pymysql.cursors.DictCursor)  # FIXED
    cur.execute(q)
    con.commit()
    result=cur.rowcount
    cur.close()
    con.close()