'''

@author: hectorz
'''
import csv
import sys
import MySQLdb
import sys

CREATETABLE = '''
Create table %s
%s  
'''
RAWDB = ''
SQLDB = r'bugzilla'


reload(sys)
sys.setdefaultencoding('utf8')
class dboperator():
    '''
    '''
    def __init__(self,db = SQLDB):
        try:
            self.conn = MySQLdb.connect("135.252.135.53","root","root",charset="utf8" )
            self.conn.ping(True)
            self.cursor = self.conn.cursor()
            self.cursor.execute("show databases")
            rows = self.cursor.fetchall()
            hasDB = False
            for row in rows:
                tmp = "%2s" % row
                print "Database %s" % tmp
                if tmp == db:
                    hasDB = True
                    break
            if not hasDB :
                self.cursor.execute('create database if not exists ' + db)
            else:
                self.cursor.execute('use '+db);
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.conn.close()
    def __del__(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
    def setConn(self,conn):
        if( conn == self.conn):
            return
        self.conn.commit()
        self.conn.close()
        self.conn = conn
    def getConn(self):
        return self.conn
                
    def insertItem(self,sql):
        self.cursor.execute(sql)
    def searchItems(self,sql):
        print sql
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def createTable(self,db_name,db_contain):
        sql = CREATETABLE %(db_name, db_contain)
        self.db_name = db_name
        sql = sql+';'
        try:
            print sql
            return self.cursor.execute(sql)
        except MySQLdb.Error, e:
            return e
    def dropTable(self, db_name ):
        sql = 'DROP TABLE IF EXISTS %s;' % db_name
        print sql
        try:
            return self.cursor.execute(sql)
        except MySQLdb.Error, e:
            return e
    def initDb(self,file):
        print file
        executor = self.cursor
        count = 0
        with open(file) as datafile:
            reader = csv.reader(datafile)
            for row in reader:
                cmd = "INSERT INTO %s VALUES (" % self.db_name
                id = row[0]
                if(id == 'ID'):
                    continue
                cmd = cmd + "'"+id.replace("'","''")+ "',"
                oDate = row[1]
                ol = [ int(x) for x in oDate.split('-')]
                cmd = cmd + "'"+("%04d-%02d-%02d"%(ol[0],ol[1],ol[2])).replace("'","''")+ "',"
                mDate = row[2]
                ol = [ int(x) for x in mDate.split('-')]
                cmd = cmd + "'"+("%04d-%02d-%02d"%(ol[0],ol[1],ol[2])).replace("'","''")+ "',"
                for item in row[3:]:
                    item = item.decode(encoding='UTF-8',errors='ignore')
                    cmd = cmd + "'"+item.replace("'","''")+ "',"
                cmd = cmd[:-1]+")"
                print cmd
                executor.execute(cmd)
                count = count+1
        return count
    
if(__name__ == "__main__"):
    db = dboperator(SQLDB)
    #db.initDb()

