
import Conn

conn = Conn.SQLServer('localhost','sa','123456','FTJXBusDb')



def getSaleOrdersCountAndPrice(time):
    '''
    获取指定日期订单总量以及合计金额
    '''
    sql='SELECT b.RealPrice from SaleOrders a,SaleOrderDetails b where a.id = b.SaleOrderId and CONVERT(varchar(100), a.OrderDate, 23)=\'{}\''.format(time)
    result = conn.ExecQuery(sql)
    TotalPrice = 0
    Count = len(result)
    for i in range(0,Count):
        TotalPrice+=result[i][0]
    return Count,TotalPrice



def getPurchaseCountAndPrice(time): 
    '''
    获取采购总量以及合计金额
    '''
    sql = 'SELECT b.PayAmount from PurchaseOrders a,Pays b where a.Id=b.PurchaseOrderId and CONVERT(varchar(100), OrderDate, 23)=\'{}\''.format(time)
    result = conn.ExecQuery(sql)
    Count = len(result)
    TotalPrice = 0
    for i in range(0,Count):
        TotalPrice+=result[i][0]
    return Count,TotalPrice

def getPaysAndBills(time):
    '''
    获取指定日期收付款情况
    '''
    sql="select PayAmount from Pays where CONVERT(varchar(100), PaymentDate, 23)=\'{}\'".format(time)
    result = conn.ExecQuery(sql)
    PayPrice = 0
    for i in range(0,len(result)):
        PayPrice+=result[i][0]
    sql="select BillAmount from Bills where CONVERT(varchar(100), PaymentDate, 23)=\'{}\'".format(time)
    result = conn.ExecQuery(sql)
    BillsPrice = 0
    for i in range(0,len(result)):
        BillsPrice+=result[i][0]
    return BillsPrice,PayPrice

    
def generate(time):
    '''
    生成邮件内容
    '''
    order = getSaleOrdersCountAndPrice(time)
    purchase = getPurchaseCountAndPrice(time)
    billpay = getPaysAndBills(time)
    text = '''时间：{0}<br/>今日销售订单情况<br/>共<a color='red'>{1}</a>单，合计金额<a color='red'>{2}</a>元。
    <br>今日采购情况订单<br/>共<a color='red'>{3}</a>单，合计金额<a color='red'>{4}</a>元。<br/>
    今日收付款情况<br/>合计收款金额<a color='red'>{5}</a>元，合计付款金额<a color='red'>{6}</a>元。
    '''.format(time,order[0],order[1],purchase[0],purchase[1],billpay[0],billpay[1])
    return text


    