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
    purchaseNum,purchasePrice,_ =getdetailPurchase(startTime,endTime) #获取采购订单数量，价格
    paysAmount,_= getdetailPays(startTime,endTime) #获取付款数目
    billsAmount,_ = getdetaillBills(startTime,endTime) #获取收款数目
    detailList = [sailOrderNum,sailOrderPrice,purchaseNum,purchasePrice,paysAmount,billsAmount]
    return detailList



def getRecord(endTime,interval):
    '''
    获取某一个时间段内，销售人员的工作业绩，即 订单数量 和 金额 
    '''

    sql = '''SELECT t1.Surname + t1.Name as UserName,count(t3.OrderCode) as OrderCount
	,sum(case when t3.IsForeignCurrency=1 then (t4.BillAmount * t3.ExchangeRate) else t4.BillAmount end) as TotalAmountRMB   
    FROM [FTJXBusDb].[ABP].[Users] t1
    join [FTJXBusDb].[ABP].UserRoles t2 on t1.Id = t2.UserId
    join [FTJXBusDb].dbo.SaleOrders t3 on t3.CreatorUserId = t1.Id
	join [FTJXBusDb].dbo.Bills t4 on t4.Id = t3.BillId
    Where t2.RoleId = 5 and t1.IsDeleted = 0 and t3.IsDeleted =0
    and t3.OrderStatus != 0 and t3.OrderDate < \'{0}\' and t3.OrderDate> dateadd(day,{1},\'{0}\') 
    and t4.IsDeleted =0 group by t1.UserName, t1.Name,t1.Surname
    order by TotalAmountRMB desc, OrderCount desc'''.format(endTime,interval)
    result = conn.ExecQuery(sql)
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>姓名</td><td>订单数量</td><td>金额</td></tr>"
    for i in result:
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0])# 姓名
        text=text+"<td>{}</td>".format(i[1])# 订单数量
        text=text+"<td>{}</td>".format(round(i[2],2))# 金额
        text+="</tr>"
    text =text+"</table>"
    return text

def generateByWeek(startTime,endTime):
    '''
    生成每周邮件内容
    '''
    detailList = getDetail(startTime,endTime)
    records = getRecord(endTime,-7)
    time = '{} 至 {}'.format(startTime.date(),endTime.date())
    text = ''' 时间：{0}<br/><b>本周销售订单情况</b><br/>共<a style="color:blue ">{1}</a>单，合计金额<a style="color:blue ">{2}</a>元。
    <br><b>今日采购情况订单</b><br/>共<a style="color:red ">{3}</a>单，合计金额<a style="color:red ">{4}</a>元。<br/>
    <b>今日收付款情况</b><br/>合计付款金额<a style="color:red ">{5}</a>元<br/>合计收款金额<a style="color:blue ">{6}</a>元。<br /><h3>人员销售业绩</h3><br>{7}
    '''.format(time,detailList[0],detailList[1],detailList[2],detailList[3],detailList[4],detailList[5],records)
    return text

if __name__ == "__main__":
    startTime = '{} 00:00:00'.format('2019-02-28')
    endTime = '{} 23:59:59'.format('2019-03-24')
    startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
    endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
    l = generateByWeek(startTime,endTime)
    with open("1234.html",mode='w') as f:
        f.write(l)
    print(l)

