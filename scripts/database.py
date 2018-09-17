import MySQLdb

class database:
    def __init__(self, host="localhost",user="root",password="",db="qrcode"):
        self.host= host
        self.user = user
        self.password = password
        self.db = db

    def connection(self, info):
        data = ''
        db = MySQLdb.connect(host=self.host,    # your host, usually localhost
                             user=self.user,         # your username
                             passwd=self.password,  # your password
                             db=self.db)        # name of the data base

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()

        # Use all the SQL you like
        cur.execute("SELECT * FROM users WHERE `serial` = '"+info+"'")

        # print all the first cell of all the rows
        for row in cur.fetchall():
            data = row

        db.close()
        return data
