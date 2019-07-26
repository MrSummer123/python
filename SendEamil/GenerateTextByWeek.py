import Conn
import datetime
from GenerateTextByDay import getdetailSailOrders,getdetailPurchase,getdetailPays,getdetaillBills

conn = Conn.SQLServer('localhost','sa','123456','FTJXBusDb')
def getDetail(startTime,endTime):
    '''
    获取销售订单数量，价格
    获取销售订单数量，价格
    获取付款数目
    获取收款数目
    '''
    detailList = []
    sailOrderNum,sailOrderPrice,_ = getdetailSailOrders(startTime,endTime) #获取销售订单数量，价格
    purchaseNum,purchasePrice,_ =getdetailPurchase(startTime,endTime) #获取销售订单数量，价格
    paysAmount,_= getdetailPays(startTime,endTime) #获取付款数目
    billsAmount,_ = getdetaillBills(startTime,endTime) #获取收款数目
    detailList = [sailOrderNum,sailOrderPrice,purchaseNum,purchasePrice,paysAmount,billsAmount]
    return detailList



def getRecord():
    '''
    获取某一个时间段内，销售人员的工作业绩，即 订单数量 和 金额 
    '''
    Now = datetime.datetime.now()
    RealTime = Now-datetime.timedelta(hours=8)
    RealTime =RealTime.strftime('%Y-%m-%d %H:%M:%S')
    sql = '''SELECT t1.Surname + t1.Name as UserName,count(t3.OrderCode) as OrderCount
	,sum(case when t3.IsForeignCurrency=1 then (t4.BillAmount * t3.ExchangeRate) else t4.BillAmount end) as TotalAmountRMB   
    FROM [FTJXBusDb].[ABP].[Users] t1
    join [FTJXBusDb].[ABP].UserRoles t2 on t1.Id = t2.UserId
    join [FTJXBusDb].dbo.SaleOrders t3 on t3.CreatorUserId = t1.Id
	join [FTJXBusDb].dbo.Bills t4 on t4.Id = t3.BillId
    Where t2.RoleId = 5 and t1.IsDeleted = 0 and t3.IsDeleted =0
    and t3.OrderStatus != 0 and t3.OrderDate < \'{0}\' and t3.OrderDate> dateadd(day,-1000,\'{0}\') 
    and t4.IsDeleted =0 group by t1.UserName, t1.Name,t1.Surname
    order by TotalAmountRMB desc, OrderCount desc'''.format(RealTime)
    result = conn.ExecQuery(sql)
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>姓名</td><td>订单数量</td><td>金额</td></tr>"
    for i in result:
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0])
        text=text+"<td>{}</td>".format(i[1])
        text=text+"<td>{}</td>".format(i[2])
        text+="</tr>"
    text =text+"</table>"
    return text

def generate(startTime,endTime):
    '''
    生成每周邮件内容
    '''
