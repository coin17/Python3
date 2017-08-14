# -*- coding:utf-8 -*-

import pymssql

class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

# ms = MSSQL(host=".",user="sa",pwd="sa",db="SmallIsBeautiful")
# reslist = ms.ExecQuery("select * from Space0002A")
# for i in reslist:
#     print(i)

# newsql="update Space0002A set column_0='%s' where id='%s'" %(u'2012年测试',u'2')
# print(newsql)
# ms.ExecNonQuery(newsql.encode('utf-8'))