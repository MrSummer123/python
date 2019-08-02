from DataAccess import DataAccess

def generateByWeek(startTime,endTime):
    '''
    生成每周邮件内容
    '''
    startTime = '{} 00:00:00'.format(startTime)
    endTime = '{} 23:59:59'.format(endTime)
    dataAccess = DataAccess()
    sailOrderNum,sailOrderPrice,_ = dataAccess.getdetailSailOrders(startTime,endTime) #获取销售订单数量，价格
    purchaseNum,purchasePrice,_ =dataAccess.getdetailPurchases(startTime,endTime) #获取采购订单数量，价格
    paysAmount,_= dataAccess.getdetailPays(startTime,endTime) #获取付款数目
    billsAmount,_ = dataAccess.getdetaillBills(startTime,endTime) #获取收款数目
    records = dataAccess.getSaleRecordOfPerson(startTime,endTime) #获取每位员工的销售情况
    time = '{} 至 {}'.format(startTime,endTime)
    text = ''' 
    时间：{0}<br/>
    <b>本周销售订单情况</b><br/>共<a style="color:blue ">{1}</a>单，
    合计金额<a style="color:blue ">{2:,}</a>元。
    <br>
    <b>本周采购情况订单</b><br/>共<a style="color:red ">{3}</a>单，
    合计金额<a style="color:red ">{4:,}</a>元。
    <br/>
    <b>本周收付款情况</b><br/>
    合计付款金额<a style="color:red ">{5:,}</a>元<br/>合计收款金额<a style="color:blue ">{6:,}</a>元。
    <br />
    <h3>人员销售业绩</h3><br>{7}
    '''.format(time,sailOrderNum,sailOrderPrice,purchaseNum,purchasePrice,paysAmount,billsAmount,records)
    return text

if __name__ == "__main__":
    startTime = '{}'.format('2019-02-25')
    endTime = '{}'.format('2019-03-03')
    l = generateByWeek(startTime,endTime)
    with open("1234.html",mode='w') as f:
        f.write(l)
    print(l)
