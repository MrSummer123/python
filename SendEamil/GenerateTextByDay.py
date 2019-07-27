
import Conn
import datetime

conn = Conn.SQLServer('localhost','sa','123456','FTJXBusDb')


def getdetailSailOrders(startTime,endTime):
    '''
    获取销售清单
    '''
    sql='''SELECT a.OrderCode,b.RealPrice,c.Name ,d.Surname+d.Name, a.IsTaxFreePay, e.Name , a.IsForeignCurrency, a.ExchangeRate
    from SaleOrders a join  SaleOrderDetails b on a.id = b.SaleOrderId 
    join Customers c on a.SaleOrderCustomer_Id = c.Id 
    join ABP.Users d  on a.ConfirmerUserId=d.Id 
    join MyCompanies e on a.MyCompanyId=e.Id
    where a.OrderDate>=\'{0}\' and a.OrderDate<=\'{1}\' 
        and a.IsDeleted=0 and a.OrderStatus=1'''.format(startTime,endTime)
    
    result = conn.ExecQuery(sql)
    Count = len(result)
    TotalPrice = 0
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>订单号</td><td>金额</td><td>客户</td><td>负责人</td><td>是否含税</td><td>公司</td></tr>"
    for i in result:
        TotalPrice += i[1]*i[7] if i[6] else i[1]
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0]) #订单号
        text=text+"<td>{}{}</td>".format('$' if i[6] else '￥',round(i[1],2)) #金额，区2位小数
        text=text+"<td>{}</td>".format(i[2]) #客户
        text=text+"<td>{}</td>".format(i[3]) #负责人
        text=text+"<td>{}</td>".format('是' if i[4] else '否') #是否含税
        text=text+"<td>{}</td>".format(i[5][2:4]) #公司名称
        # for j in range(0,len(i)):
        #     if j==1:
        #         TotalPrice += i[j]
        #         s = i[j]
        #         text+= "<td>{}</td>".format(round(s,2))
        #     else:
        #         text=text+"<td>{}</td>".format(i[j])
        text+="</tr>"
    text =text+"</table>"
    return Count,round(TotalPrice,2),text




def getdetailPurchase(startTime,endTime):
    '''
    获取采购清单
    '''
    sql='''SELECT  a.OrderCode,b.PayAmount,c.Name,d.Surname+d.Name, a.IsTaxFreePay, e.Name , a.IsForeignCurrency, a.ExchangeRate
    from PurchaseOrders a join Pays b on a.Id=b.PurchaseOrderId 
    join Suppliers c on a.PurchaseOrderSupplier_Id=c.Id 
    join  ABP.Users d on a.ConfirmerUserId = d.Id 
    join MyCompanies e on a.MyCompanyId=e.Id
    where a.OrderDate>=\'{0}\' and a.OrderDate<=\'{1}\' and a.IsDeleted=0 and a.OrderStatus=1'''.format(startTime,endTime)
    result = conn.ExecQuery(sql)
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>订单号</td><td>金额</td><td>经销商</td><td>负责人</td><td>是否含税</td><td>公司</td></tr>"
    Count = len(result)
    TotalPrice = 0
    for i in result:
        TotalPrice += i[1]*i[7] if i[6] else i[1]
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0]) #订单号
        text=text+"<td>{}{}</td>".format('$' if i[6] else '￥',round(i[1],2)) #金额，区2位小数
        text=text+"<td>{}</td>".format(i[2]) #经销商
        text=text+"<td>{}</td>".format(i[3]) #负责人
        text=text+"<td>{}</td>".format('是' if i[4] else '否') #是否含税
        text=text+"<td>{}</td>".format(i[5][2:4]) #公司名称
        text+"</tr>"
    text =text+"</table>"
    return Count,round(TotalPrice,2), text



def getdetailPays(startTime,endTime):
    '''
    获取付款清单
    '''
    sql='''select a.SerialNumber, b.PayName,a.Amount,a.PaymentParty, d.Surname+d.Name, a.AmountRMB ,a.IsForeignCurrency
    from FinanceRecords a join Pays b on a.PayId = b.Id
    join ABP.Users d on a.CreatorUserId = d.Id
    where a.PaymentTime>=\'{0}\' and a.PaymentTime<=\'{1}\' and a.IsDeleted=0'''.format(startTime,endTime)
    result = conn.ExecQuery(sql)
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>流水号</td><td>名称</td><td>金额</td><td>收款方</td><td>经办人</td></tr>"
    PayPrice = 0
    for i in result:
        PayPrice += i[5]
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0]) #流水号
        text=text+"<td>{}</td>".format(i[1]) #名称
        text=text+"<td>{}{}</td>".format('$' if i[6] else '￥',round(i[2],2)) #金额，区2位小数
        text=text+"<td>{}</td>".format(i[3]) #付款方
        text=text+"<td>{}</td>".format(i[4]) #经办人        
        text+"</tr>"
    text =text+"</table>"
    return round(PayPrice,2),text




def getdetaillBills(startTime,endTime):
    '''
    获取收款清单
    '''

    sql='''select a.SerialNumber,  b.BillName, a.Amount,a.PaymentParty, d.Surname+d.Name, a.AmountRMB ,a.IsForeignCurrency
    from FinanceRecords a join  Bills b on  a.BillId = b.Id 
    join ABP.Users d on a.CreatorUserId = d.Id 
    where a.PaymentTime>=\'{0}\' and a.PaymentTime<=\'{1}\' and a.IsDeleted=0'''.format(startTime,endTime)

    result = conn.ExecQuery(sql)
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>流水号</td><td>名称</td><td>金额</td><td>付款方</td><td>经办人</td></tr>"
    BillsPrice = 0
    for i in result:
        BillsPrice += i[5]
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0]) #流水号
        text=text+"<td>{}</td>".format(i[1]) #名称
        text=text+"<td>{}{}</td>".format('$' if i[6] else '￥',round(i[2],2)) #金额，区2位小数
        text=text+"<td>{}</td>".format(i[3]) #付款方
        text=text+"<td>{}</td>".format(i[4]) #经办人        
        text+"</tr>"
    text =text+"</table>"
    return round(BillsPrice,2), text


def getOrderByReceived():
    '''
    获取已经到期收款但是没有收款完毕的订单信息
    '''
    Now = datetime.datetime.now()
    RealTime = Now-datetime.timedelta(hours=8)
    RealTime =RealTime.strftime('%Y-%m-%d %H:%M:%S')
    sql='''SELECT t1.[OrderCode],t3.UserName,t4.Name as CustomerName,case when t1.IsForeignCurrency=1 then 'USD' else 'RMB' end as Currency
	,t2.BillAmount
	,t2.BillReceivedAmount
	,t2.BillAmount - t2.BillReceivedAmount as  DiffAmount
	,RequireFinalPayDate
	,DATEDIFF(day,t1.RequireFinalPayDate,\'{0}\') as ExpiredDays
    FROM [FTJXBusDb].[dbo].[SaleOrders] t1
    join [FTJXBusDb].[dbo].Bills t2 on t1.BillId = t2.Id
    join [FTJXBusDb].[ABP].Users t3 on t1.CreatorUserId = t3.Id
    join [FTJXBusDb].dbo.Customers t4 on t1.SaleOrderCustomer_Id = t4.Id 
    WHERE RequireFinalPayDate < \'{0}\'
    and t2.PaymentStatus != 2
    and t1.OrderStatus = 1 
    and t1.IsDeleted = 0
    and t2.BillAmount > 0 
    and t2.IsDeleted = 0
    ORDER BY t1.OrderDate desc'''.format(RealTime)
    result = conn.ExecQuery(sql)
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>订单号</td><td>经办人</td><td>客户名</td><td>货币</td><td>账单金额</td><td>已收金额</td><td>待收金额</td><td>付款期限</td><td>已超期天数</td></tr>"
    for i in result:   
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0]) #订单号
        text=text+"<td>{}</td>".format(i[1]) #经办人
        text=text+"<td>{}</td>".format(i[2]) #客户名
        text=text+"<td>{}</td>".format(i[3]) #货币
        text=text+"<td>{}</td>".format(i[4]) #账单金额
        text=text+"<td>{}</td>".format(i[5]) #已收金额
        text=text+"<td>{}</td>".format(i[6]) #待收金额
        text=text+"<td>{}</td>".format(i[7].strftime('%Y-%m-%d')) #付款期限
        text=text+"<td>{}</td>".format(i[8]) #已超期天数
        text+"</tr>"
    text =text+"</table>"
    return text
   

def getProductByDate():
    '''
    获取到期但未发货的产品
    '''
    Now = datetime.datetime.now()
    RealTime = Now-datetime.timedelta(hours=8)
    RealTime =RealTime.strftime('%Y-%m-%d %H:%M:%S')
    sql='''SELECT t2.OrderCode,t7.Name ,case when t2.PaymentMode=0 then '款到发货' when t2.PaymentMode=1 then  '货到付款' end as PaymentMode
	,t6.UserName,t3.ProductCode,t5.BrandName,t1.[OrderNumber],t1.[RealPrice] ,t1.[NumberShiped] ,t1.RequestedShipDate
	,DATEDIFF(day,t1.RequestedShipDate,\'{0}\') as ExpiredDays
    FROM [FTJXBusDb].[dbo].[SaleOrderDetails] as t1  
    join  [FTJXBusDb].[dbo].SaleOrders as t2 on t1.SaleOrderId = t2.Id  
	join  [FTJXBusDb].[dbo].Products t3 on t1.ProductId = t3.Id 
	join [FTJXBusDb].[dbo].ProductTypes t4 on t3.ProductType_Id = t4.Id 
	join [FTJXBusDb].[dbo].Brands t5 on t4.TypeBrand_Id = t5.Id 
	join [FTJXBusDb].[ABP].Users t6 on t2.CreatorUserId = t6.Id 
	join [FTJXBusDb].dbo.Customers t7 on t2.SaleOrderCustomer_Id = t7.Id 
	join [FTJXBusDb].dbo.Bills t8 on t2.BillId = t8.Id 
    where t1.NumberShiped != t1.OrderNumber 
    and t1.IsDeleted = 0 
    and RequestedShipDate < \'{0}\'
    and t2.OrderStatus =1  
    and t2.IsDeleted = 0
    and (t2.PaymentMode = 1 or (t2.PaymentMode =0 and t8.BillReceivedAmount>0)) 
    order by t2.OrderDate desc, t2.OrderCode '''.format(RealTime)
    result = conn.ExecQuery(sql)
    text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>订单号</td><td>客户名</td><td>付款方式</td><td>经办人</td><td>产品号</td><td>商标名</td><td>订购数量</td><td>原价</td><td>已发数量</td><td>限期</td><td>已超期天数</td></tr>"
    for i in result:   
        text = text+"<tr>"
        text=text+"<td>{}</td>".format(i[0]) #订单号
        text=text+"<td>{}</td>".format(i[1]) #客户名
        text=text+"<td>{}</td>".format(i[2]) #付款方式
        text=text+"<td>{}</td>".format(i[3]) #经办人
        text=text+"<td>{}</td>".format(i[4]) #产品号
        text=text+"<td>{}</td>".format(i[5]) #商标名
        text=text+"<td>{}</td>".format(i[6]) #订购数量
        text=text+"<td>{}</td>".format(round(i[7],2)) #原价
        text=text+"<td>{}</td>".format(i[8]) #已发数量
        text=text+"<td>{}</td>".format(i[9].strftime('%Y-%m-%d')) #限期
        text=text+"<td>{}</td>".format(i[10])  #已超期天数 
        text+"</tr>"
    text =text+"</table>"
    return text



    
def generate(startTime,endTime):
    '''
    生成每日邮件内容
    '''
    time = '{} 至 {}'.format(startTime.date(),endTime.date())
    orderNum, OrderpriceNum ,detailsail = getdetailSailOrders(startTime,endTime)
    purchaseNum, purchasepriceNum,detailpur = getdetailPurchase(startTime,endTime)
    billprice, detailbills = getdetaillBills(startTime,endTime)
    purchaseprice,detailpays = getdetailPays(startTime,endTime)
    OrderbyReceived = getOrderByReceived()
    ProductByDate=getProductByDate()
    text = '''时间：{0}<br/><b>今日销售订单情况</b><br/>共<a style="color:blue ">{1}</a>单，合计金额<a style="color:blue ">{2}</a>元。
    <br><b>今日采购情况订单</b><br/>共<a style="color:red ">{3}</a>单，合计金额<a style="color:red ">{4}</a>元。<br/>
    <b>今日收付款情况</b><br/>合计付款金额<a style="color:red ">{5}</a>元<br/>合计收款金额<a style="color:blue ">{6}</a>元。<br /><h3>销售清单</h3><br>
    {7}<br /><h3>采购清单</h3><br>{8}<br /><h3>收款清单</h3><br>{9}<br /><h3>付款清单</h3><br>{10}<br />
    <h3>已到期收款但未收款完毕订单信息</h3><br>{11}<br /> <h3> 到期但未发货的产品</h3>{12}
    '''.format(time,orderNum,OrderpriceNum,purchaseNum,purchasepriceNum,purchaseprice,billprice,detailsail,detailpur,detailbills,detailpays,OrderbyReceived,ProductByDate)
    return text




if __name__ == "__main__":
    startTime = '{} 00:00:00'.format('2019-02-28')
    endTime = '{} 23:59:59'.format('2019-02-28')
    startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
    endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)

    l = generate(startTime,endTime)
    with open("123.html",mode='w') as f:
        f.write(l)
    print(l)
