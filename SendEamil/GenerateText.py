import datetime
import Conn

conn = Conn.SQLServer('localhost','sa','123456','FTJXBusDb')
def getTotalCount():
    sql = 'select OrderDate from SaleOrders'
    result = conn.ExecQuery(sql)
    # time = str(datetime.date.today())
    time = '2018-11-12'
    TotalCount = 0 
    for i in range(0,len(result)):
        stime = list(result[i])[0].strftime("%Y-%m-%d")
        if stime==time:
            TotalCount+=1
    return TotalCount



