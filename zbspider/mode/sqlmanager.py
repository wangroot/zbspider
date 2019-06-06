import sqlite3
from ..settings import DATABASE
from . import dbprint

class SQLManager(object):
    __tablename__ = "zbtable"

    def __init__(self): 
        #实例化后自动执行此函数
        self.connect()
        try:
            self.create()
            dbprint("created table successfully")
        except:
            dbprint("created table failed")

    def connect(self): 
        # 进入数据库，创建游标
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()
        dbprint("Opened database successfully")
        
    def create(self):
        # 创建数据表
        _sql = "CREATE TABLE IF NOT EXISTS "+ self.__tablename__ + \
               " (ID INTEGER PRIMARY KEY NOT NULL," +\
                 "TITLE VARCHAR(255) NOT NULL," + \
                 "LINK VARCHAR(255) NOT NULL," + \
                 "TIME VARCHAR(255) NOT NULL" + \
                ");"
        self.cursor.execute(_sql)
        self.conn.commit()

    def insert(self, data):
        # 插入数据
        _sql = "INSERT INTO "+ self.__tablename__ +" (TITLE,LINK,TIME)" +\
               " VALUES ('"+data['title']+"', '"+data['link']+"', '"+data['time']+"');"
        # print(_sql)
        self.cursor.execute(_sql)
        self.conn.commit()

    def get_last_one_title(self):
        # 获取id最大的数据
        _sql = "SELECT TITLE,LINK,TIME FROM "+ self.__tablename__ + \
               " WHERE ID=(SELECT MAX(ID) FROM "+ self.__tablename__ + \
               ");"
        # print(_sql)
        self.cursor.execute(_sql)
        result = self.cursor.fetchone()
        _dict = {
            'title': result[0],
            'link': result[1],
            'time': result[2]
        }
        return _dict

    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def run(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
        dbprint("database closed")