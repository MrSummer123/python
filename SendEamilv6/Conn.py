# coding=utf-8
import pymssql

class SQLServer:
    def __init__(self,server,user,password,database):
    # 类的构造函数，初始化DBC连接信息
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def __GetConnect(self):
    # 得到数据库连接信息，返回conn.cursor()
        if not self.database:
            raise(NameError,"没有设置数据库信息")
        try:
            self.conn = pymssql.connect(server=self.server,user=self.user,password=self.password,database=self.database)
        except:
            raise(ConnectionError,"连接出错")
        
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")  # 将DBC信息赋值给cur
        else:
            return cur
             
    def ExecQuery(self,sql):
        '''
        执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        '''
        cur = self.__GetConnect()
        cur.execute(sql) # 执行查询语句
        result = cur.fetchall() # fetchall()获取查询结果
        # 查询完毕关闭数据库连接
        self.conn.close()
        return result
    def ExecNonQuery(self,sql):
        '''
        执行非查询语句
        '''
        cur = self.__GetConnect()
        cur.execute(sql)  # 执行查询语句
        self.conn.commit()
        # 查询完毕关闭数据库连接
        self.conn.close()
    def ExecNonQueryMany(self,sql,datalist):
        '''
        针对datalist中的数据，执行多条非查询语句
        sql形式为INSERT INTO persons VALUES (%d, %s, %s)
        datalist是一个列表，每个元素是一个元组，对应与上面的%占位符
        '''
        cur = self.__GetConnect()
        cur.executemany(sql,datalist)  # 执行查询语句
        self.conn.commit()
        # 查询完毕关闭数据库连接
        self.conn.close()