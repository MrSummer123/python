
import Conn
import datetime
class DataAccess():
    def __init__(self,filename='login.txt'):
        self.conn = None
        try:
            with open(filename,'r') as fp:
                url,username, pwd, database = fp.readlines()[0].strip().split(',')
            self.conn = Conn.SQLServer(url,username,pwd,database)
        except:
            raise("Error")
    def getdetailSailOrders(self,startTime,endTime):
        '''
        获取时间区域内的销售清单，返回值为销售订单数量，合计价格，和详细表格（html表格）
        '''
        #进行时区调整
        startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)

        sql = '''SELECT a.OrderCode,b.BillAmount,c.Name ,d.Surname+d.Name, a.IsTaxFreePay,
        e.Name , a.IsForeignCurrency, a.ExchangeRate
        from SaleOrders a
        join Bills b on  b.Id = a.BillId  
        join Customers c on a.SaleOrderCustomer_Id = c.Id 
        join ABP.Users d  on a.CreatorUserId=d.Id 
        join MyCompanies e on a.MyCompanyId=e.Id
        where a.OrderDate>=\'{0}\' and a.OrderDate<=\'{1}\'
        and a.IsDeleted=0 and a.OrderStatus != 0'''.format(startTime, endTime)
        
        result = self.conn.ExecQuery(sql)
        count = len(result)
        totalPrice = 0
        text ='''<table width='100%' border='1' cellpadding='0' cellspacing='0' 
        style='border-collapse:collapse;'> 
        <tr><td>订单号</td><td>金额</td><td>客户</td><td>经办人</td><td>是否含税</td><td>公司</td></tr>'''
        for i in result:
            totalPrice += i[1]*i[7] if i[6] else i[1]
            text = text+"<tr>"
            text=text+"<td>{}</td>".format(i[0]) #订单号
            text=text+"<td>{}{:,}</td>".format('$' if i[6] else '￥',round(i[1],2)) #金额，区2位小数
            text=text+"<td>{}</td>".format(i[2]) #客户
            text=text+"<td>{}</td>".format(i[3]) #负责人
            text=text+"<td>{}</td>".format('是' if i[4] else '否') #是否含税
            text=text+"<td>{}</td>".format(i[5][2:4]) #公司名称
            text+="</tr>"
        text =text+"</table>"
        return count,round(totalPrice,2),text


    def getdetailPurchases(self,startTime,endTime):
        '''
        获取时间区域内的采购清单，返回值为采购订单数量，合计价格，和详细表格（html表格）
        '''
        #进行时区调整
        startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        sql='''SELECT  a.OrderCode,b.PayAmount,c.Name,d.Surname+d.Name, a.IsTaxFreePay, e.Name , a.IsForeignCurrency, a.ExchangeRate
        from PurchaseOrders a join Pays b on b.Id = a.PayId
        join Suppliers c on a.PurchaseOrderSupplier_Id=c.Id 
        join  ABP.Users d on a.ConfirmerUserId = d.Id 
        join MyCompanies e on a.MyCompanyId=e.Id
        where a.OrderDate>=\'{0}\' and a.OrderDate<=\'{1}\'
        and a.IsDeleted=0 and a.OrderStatus !=0'''.format(startTime,endTime)
        result = self.conn.ExecQuery(sql)
        text ='''<table width='100%' border='1' cellpadding='0' cellspacing='0' 
        style='border-collapse:collapse;'> 
        <tr><td>订单号</td><td>金额</td><td>经销商</td><td>经办人</td><td>是否含税</td><td>公司</td></tr>'''
        Count = len(result)
        TotalPrice = 0
        for i in result:
            TotalPrice += i[1]*i[7] if i[6] else i[1]
            text = text+"<tr>"
            text=text+"<td>{}</td>".format(i[0]) #订单号
            text=text+"<td>{}{:,}</td>".format('$' if i[6] else '￥',round(i[1],2)) #金额，区2位小数
            text=text+"<td>{}</td>".format(i[2]) #经销商
            text=text+"<td>{}</td>".format(i[3]) #负责人
            text=text+"<td>{}</td>".format('是' if i[4] else '否') #是否含税
            text=text+"<td>{}</td>".format(i[5][2:4]) #公司名称
            text+"</tr>"
        text =text+"</table>"
        return Count,round(TotalPrice,2), text

    def getdetailPays(self,startTime,endTime):
        '''
        获取指定时间范围内的付款详情，返回值为付款总金额，付款详情表格（html）
        '''
        #进行时区调整
        startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        sql='''select a.SerialNumber, b.PayName,a.Amount,a.PaymentParty, d.Surname+d.Name, a.AmountRMB ,a.IsForeignCurrency
        from FinanceRecords a join Pays b on a.PayId = b.Id
        join ABP.Users d on a.CreatorUserId = d.Id
        where a.PaymentTime>=\'{0}\' and a.PaymentTime<=\'{1}\' and a.IsDeleted=0'''.format(startTime,endTime)
        result = self.conn.ExecQuery(sql)
        text ='''<table width='100%' border='1' cellpadding='0' cellspacing='0' 
        style='border-collapse:collapse;'> 
        <tr><td>流水号</td><td>名称</td><td>金额</td><td>收款方</td><td>经办人</td></tr>'''
        totalPayPrice = 0
        for i in result:
            totalPayPrice += i[5]
            text = text+"<tr>"
            text=text+"<td>{}</td>".format(i[0]) #流水号
            text=text+"<td>{}</td>".format(i[1]) #名称
            text=text+"<td>{}{:,}</td>".format('$' if i[6] else '￥',round(i[2],2)) #金额，区2位小数
            text=text+"<td>{}</td>".format(i[3]) #付款方
            text=text+"<td>{}</td>".format(i[4]) #经办人
            text+"</tr>"
        text =text+"</table>"
        return round(totalPayPrice,2),text

    def getdetaillBills(self,startTime,endTime):
        '''
        获取指定时间范围内的收款详情，返回值为收款总金额，付款详情表格（html）
        '''
        #进行时区调整
        startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        sql='''select a.SerialNumber,  b.BillName, a.Amount,a.PaymentParty, d.Surname+d.Name, a.AmountRMB ,a.IsForeignCurrency
        from FinanceRecords a join  Bills b on  a.BillId = b.Id 
        join ABP.Users d on a.CreatorUserId = d.Id 
        where a.PaymentTime>=\'{0}\' and a.PaymentTime<=\'{1}\' and a.IsDeleted=0'''.format(startTime,endTime)

        result = self.conn.ExecQuery(sql)
        text ='''<table width='100%' border='1' cellpadding='0' cellspacing='0' 
        style='border-collapse:collapse;'> 
        <tr><td>流水号</td><td>名称</td><td>金额</td><td>付款方</td><td>经办人</td></tr>'''
        totalBillPrice = 0
        for i in result:
            totalBillPrice += i[5]
            text = text+"<tr>"
            text=text+"<td>{}</td>".format(i[0]) #流水号
            text=text+"<td>{}</td>".format(i[1]) #名称
            text=text+"<td>{}{:,}</td>".format('$' if i[6] else '￥',round(i[2],2)) #金额，区2位小数
            text=text+"<td>{}</td>".format(i[3]) #付款方
            text=text+"<td>{}</td>".format(i[4]) #经办人
            text+"</tr>"
        text =text+"</table>"
        return round(totalBillPrice,2), text

    def getSaleOrders_MoneyExpired(self):
        '''
        获取已经到期收款但是没有收款完毕的订单信息
        '''
        Now = datetime.datetime.now()
        RealTime = Now-datetime.timedelta(hours=8)
        RealTime =RealTime.strftime('%Y-%m-%d %H:%M:%S')
        sql='''SELECT t1.[OrderCode],t3.Surname + t3.Name as UserName,t4.Name as CustomerName,case when t1.IsForeignCurrency=1 then 'USD' else 'RMB' end as Currency
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
        result = self.conn.ExecQuery(sql)
        text ="<table width='100%' border='1' cellpadding='0' cellspacing='0' style='border-collapse:collapse;'> <tr><td>订单号</td><td>经办人</td><td>客户名</td><td>货币</td><td>账单金额</td><td>已收金额</td><td>待收金额</td><td>付款期限</td><td>已超期天数</td></tr>"
        for i in result:   
            text = text+"<tr>"
            text=text+"<td>{}</td>".format(i[0]) #订单号
            text=text+"<td>{}</td>".format(i[1]) #经办人
            text=text+"<td>{}</td>".format(i[2]) #客户名
            text=text+"<td>{}</td>".format(i[3]) #货币
            text=text+"<td>{:,}</td>".format(i[4]) #账单金额
            text=text+"<td>{:,}</td>".format(i[5]) #已收金额
            text=text+"<td>{:,}</td>".format(i[6]) #待收金额
            text=text+"<td>{}</td>".format(i[7].strftime('%Y-%m-%d')) #付款期限
            text=text+"<td>{}</td>".format(i[8]) #已超期天数
            text+"</tr>"
        text =text+"</table>"
        return text
    

    def getProducts_ShipExpired(self):
        '''
        获取已经到期发货但未发货完毕的产品
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
        result = self.conn.ExecQuery(sql)
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
            text=text+"<td>{:,}</td>".format(round(i[7],2)) #原价
            text=text+"<td>{}</td>".format(i[8]) #已发数量
            text=text+"<td>{}</td>".format(i[9].strftime('%Y-%m-%d')) #限期
            text=text+"<td>{}</td>".format(i[10])  #已超期天数 
            text+"</tr>"
        text =text+"</table>"
        return text

    def getSaleRecordOfPerson(self,startTime,endTime):
        '''
        获取某一个时间段内，销售人员的工作业绩，即 订单数量 和 金额 
        '''
        startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
        endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)

        sql = '''SELECT   t1.Surname + t1.Name as UserName
        ,count(t3.OrderCode) as OrderCount
        ,sum(case when t3.IsForeignCurrency=1 then (t4.BillAmount * t3.ExchangeRate) else t4.BillAmount end) as TotalAmountRMB   
        FROM [FTJXBusDb].[ABP].[Users] t1
            join [FTJXBusDb].dbo.SaleOrders t3 on t3.CreatorUserId = t1.Id
            join [FTJXBusDb].dbo.Bills t4 on t4.Id = t3.BillId
        Where t1.IsDeleted = 0
        and t3.IsDeleted =0
        and t3.OrderStatus != 0 
        and t3.OrderDate >= \'{0}\' and t3.OrderDate<= \'{1}\'
        and t4.IsDeleted =0
        group by t1.UserName, t1.Name,t1.Surname
        order by TotalAmountRMB desc, OrderCount desc'''.format(startTime,endTime)
        result = self.conn.ExecQuery(sql)
        text ='''<table width='100%' border='1' cellpadding='0' cellspacing='0' 
        style='border-collapse:collapse;'> <tr><td>姓名</td><td>订单数量</td><td>金额</td></tr>'''
        for i in result:
            text = text+"<tr>"
            text=text+"<td>{}</td>".format(i[0])# 姓名
            text=text+"<td>{}</td>".format(i[1])# 订单数量
            text=text+"<td>{:,}</td>".format(round(i[2],2))# 金额
            text+="</tr>"
        text =text+"</table>"
        return text