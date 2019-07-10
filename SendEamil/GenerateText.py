
import Conn

conn = Conn.SQLServer('localhost','sa','123456','FTJXBusDb')



# def getSaleOrdersCountAndPrice(time):
#     '''
#     获取指定日期销售订单总量以及合计金额
#     '''
#     sql='SELECT b.RealPrice from SaleOrders a,SaleOrderDetails b where a.id = b.SaleOrderId and CONVERT(varchar(100), a.OrderDate, 23)=\'{}\''.format(time)
#     result = conn.ExecQuery(sql)
#     TotalPrice = 0
#     Count = len(result)
#     for i in range(0,Count):
#         TotalPrice+=result[i][0]
#     return Count,TotalPrice


def getdetailSailOrders(time):
    '''
    获取销售清单
    '''
    sql='SELECT a.OrderCode,b.RealPrice,c.Name ,d.Surname+d.Name from SaleOrders a,SaleOrderDetails b,Customers c ,ABP.Users d  where a.id = b.SaleOrderId and a.SaleOrderCustomer_Id = c.Id and a.ConfirmerUserId=d.Id  and CONVERT(varchar(100), a.OrderDate, 23)=\'{}\''.format(time)
    result = conn.ExecQuery(sql)
    Count = len(result)
    TotalPrice = 0
    text ="<table border='1' width='700'> <tr><td>订单号</td><td>金额</td><td>客户</td><td>负责人</td></tr>"
    for i in result:
        text = text+"<tr>"
        for j in range(0,len(i)):
            if j==1:
                TotalPrice += i[j]
            text=text+"<td>{}</td>".format(i[j])
        text+"</tr>"
    text =text+"</table>"
    return Count,TotalPrice,text



# def getPurchaseCountAndPrice(time): 
#     '''
#     获取采购总量以及合计金额
#     '''
#     sql = 'SELECT b.PayAmount from PurchaseOrders a,Pays b where a.Id=b.PurchaseOrderId and CONVERT(varchar(100), OrderDate, 23)=\'{}\''.format(time)
#     result = conn.ExecQuery(sql)
#     Count = len(result)
#     TotalPrice = 0
#     for i in range(0,Count):
#         TotalPrice+=result[i][0]
#     return Count,TotalPrice

def getdetailPurchase(time):
    '''
    获取采购清单
    '''
    sql="SELECT  a.OrderCode,b.PayAmount,c.Name,d.Surname+d.Name from PurchaseOrders a,Pays b,Suppliers c,ABP.Users d where a.Id=b.PurchaseOrderId and a.PurchaseOrderSupplier_Id=c.Id and a.ConfirmerUserId = d.Id and CONVERT(varchar(100), OrderDate, 23)=\'{}\'".format(time)
    result = conn.ExecQuery(sql)
    text ="<table border='1' width='700'> <tr><td>订单号</td><td>金额</td><td>经销商</td><td>负责人</td></tr>"
    Count = len(result)
    TotalPrice = 0
    for i in result:
        text = text+"<tr>"
        for j in range(0,len(i)):
            if j==1:
                TotalPrice+=i[j]
            text=text+"<td>{}</td>".format(i[j])
        text+"</tr>"
    text =text+"</table>"
    return Count,TotalPrice, text

# def getPaysAndBills(time):
#     '''
#     获取指定日期收付款情况
#     '''
#     sql="select PayAmount from Pays where CONVERT(varchar(100), PaymentDate, 23)=\'{}\'".format(time)
#     result = conn.ExecQuery(sql)
#     PayPrice = 0
#     for i in range(0,len(result)):
#         PayPrice+=result[i][0]
#     sql="select BillReceivedAmount from Bills where CONVERT(varchar(100), PaymentDate, 23)=\'{}\'".format(time)
#     result = conn.ExecQuery(sql)
#     BillsPrice = 0
#     for i in range(0,len(result)):
#         BillsPrice+=result[i][0]
#     return BillsPrice,PayPrice


def getdetailPays(time):
    '''
    获取付款清单
    '''
    sql='select d.SerialNumber,  PayName, PayAmount,c.Name, e.Surname+e.Name from Pays a,PurchaseOrders b,Suppliers c,FinanceRecords d ,ABP.Users e where a.Id = b.PayId and b.PurchaseOrderSupplier_Id=c.Id and a.Id = d.PayId and d.CreatorUserId = e.Id and CONVERT(varchar(100), a.PaymentDate, 23)=\'{}\''.format(time)
    result = conn.ExecQuery(sql)
    text ="<table border='1' width='900'> <tr><td>流水号</td><td>名称</td><td>金额</td><td>付款方</td><td>经办人</td></tr>"
    PayPrice = 0
    for i in result:
        text = text+"<tr>"
        for j in range(0,len(i)):
            if j==2:
                PayPrice += i[j]
            text=text+"<td>{}</td>".format(i[j])
        text+"</tr>"
    text =text+"</table>"
    return PayPrice,text


def getdetaillBills(time):
    '''
    获取收款清单
    '''
    sql='select d.SerialNumber,  BillName, BillReceivedAmount,c.Name, e.Surname+e.Name from Bills a,SaleOrders b,Customers c,FinanceRecords d ,ABP.Users e where a.Id = b.BillId and b.SaleOrderCustomer_Id=c.Id and a.Id = d.BillId and d.CreatorUserId = e.Id and CONVERT(varchar(100), a.PaymentDate, 23)=\'{}\''.format(time)
    result = conn.ExecQuery(sql)
    text ="<table border='1' width='900'> <tr><td>流水号</td><td>名称</td><td>金额</td><td>收款方</td><td>经办人</td></tr>"
    BillsPrice = 0
    for i in result:
        text = text+"<tr>"
        for j in range(0,len(i)):
            if j==2:
                BillsPrice += i[j]
            text=text+"<td>{}</td>".format(i[j])
        text+"</tr>"
    text =text+"</table>"
    return BillsPrice, text





    
def generate(time):
    '''
    生成邮件内容
    '''
    orderNum, OrderpriceNum ,detailsail = getdetailSailOrders(time)
    purchaseNum, purchasepriceNum,detailpur = getdetailPurchase(time)
    purchaseprice, detailbills = getdetaillBills(time)
    billpayprice,detailpays = getdetailPays(time)
    text = '''时间：{0}<br/>今日销售订单情况<br/>共<a style="color:red ">{1}</a>单，合计金额<a style="color:red ">{2}</a>元。
    <br>今日采购情况订单<br/>共<a style="color:red ">{3}</a>单，合计金额<a style="color:red ">{4}</a>元。<br/>
    今日收付款情况<br/>合计付款金额<a style="color:red ">{5}</a>元，合计收款金额<a style="color:red ">{6}</a>元。<br /><h3>销售清单</h3><br>
    {7}<br /><h3>采购清单</h3><br>{8}<br /><h3>付款清单</h3><br>{9}<br /><h3>收款清单</h3><br>{10}
    '''.format(time,orderNum,OrderpriceNum,purchaseNum,purchasepriceNum,purchaseprice,billpayprice,detailsail,detailpur,detailbills,detailpays)
    return text

 