
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
    #sql='select d.SerialNumber,  BillName, BillReceivedAmount,c.Name, e.Surname+e.Name from Bills a join  SaleOrders b on  a.Id = b.BillId join  Customers c on b.SaleOrderCustomer_Id=c.Id join FinanceRecords d on a.Id = d.BillId  join ABP.Users e on d.CreatorUserId = e.Id where a.PaymentDate>=\'{0}\' and a.PaymentDate<=\'{1}\' and a.IsDeleted=0'.format(startTime,endTime)
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

    
def generate(startTime,endTime):
    '''
    生成邮件内容
    '''
    time = '{} 至 {}'.format(startTime.date(),endTime.date())
    orderNum, OrderpriceNum ,detailsail = getdetailSailOrders(startTime,endTime)
    purchaseNum, purchasepriceNum,detailpur = getdetailPurchase(startTime,endTime)
    billprice, detailbills = getdetaillBills(startTime,endTime)
    purchaseprice,detailpays = getdetailPays(startTime,endTime)
    text = '''时间：{0}<br/><b>今日销售订单情况</b><br/>共<a style="color:blue ">{1}</a>单，合计金额<a style="color:blue ">{2}</a>元。
    <br><b>今日采购情况订单</b><br/>共<a style="color:red ">{3}</a>单，合计金额<a style="color:red ">{4}</a>元。<br/>
    <b>今日收付款情况</b><br/>合计付款金额<a style="color:red ">{5}</a>元<br/>合计收款金额<a style="color:blue ">{6}</a>元。<br /><h3>销售清单</h3><br>
    {7}<br /><h3>采购清单</h3><br>{8}<br /><h3>收款清单</h3><br>{9}<br /><h3>付款清单</h3><br>{10}
    '''.format(time,orderNum,OrderpriceNum,purchaseNum,purchasepriceNum,purchaseprice,billprice,detailsail,detailpur,detailbills,detailpays)
    return text


# time = '2019-01-30'
# startTime = '{} 00:00:00'.format(time)
# endTime = '{} 23:59:59'.format(time)
# startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
# endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)

# l = generate(startTime,endTime)
# print(l)
if __name__ == "__main__":
    startTime = '{} 00:00:00'.format('2019-02-28')
    endTime = '{} 23:59:59'.format('2019-02-28')
    startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
    endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)

    l = generate(startTime,endTime)
    with open("123.html",mode='w') as f:
        f.write(l)
    print(l)
