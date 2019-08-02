from DataAccess import DataAccess
def generate(startTime,endTime):
    '''
    生成每日邮件内容
    '''
    startTime = '{} 00:00:00'.format(startTime)
    endTime = '{} 23:59:59'.format(endTime)
    dataAccess = DataAccess()
    
    time = '{} 至 {}'.format(startTime,endTime)
    orderNum, OrderpriceNum ,detailsail = dataAccess.getdetailSailOrders(startTime,endTime)
    purchaseNum, purchasepriceNum,detailpur = dataAccess.getdetailPurchases(startTime,endTime)
    billprice, detailbills = dataAccess.getdetaillBills(startTime,endTime)
    purchaseprice,detailpays = dataAccess.getdetailPays(startTime,endTime)
    saleOrdersMoneyExpired = dataAccess.getSaleOrders_MoneyExpired()
    productsShipExpired= dataAccess.getProducts_ShipExpired()
    text = '''时间：{0}<br/><b>今日销售订单情况</b><br/>共<a style="color:blue ">{1}</a>单，合计金额<a style="color:blue ">{2}</a>元。
    <br><b>今日采购情况订单</b><br/>共<a style="color:red ">{3}</a>单，合计金额<a style="color:red ">{4}</a>元。<br/>
    <b>今日收付款情况</b><br/>合计付款金额<a style="color:red ">{5}</a>元<br/>合计收款金额<a style="color:blue ">{6}</a>元。<br /><h3>销售清单</h3><br>
    {7}<br /><h3>采购清单</h3><br>{8}<br /><h3>收款清单</h3><br>{9}<br /><h3>付款清单</h3><br>{10}<br />
    <h3>到期未收款订单信息</h3><br>{11}<br /> <h3> 到期未发货的产品信息</h3>{12}
    '''.format(time,orderNum,OrderpriceNum,purchaseNum,purchasepriceNum,purchaseprice,billprice,detailsail,detailpur,detailbills,detailpays,saleOrdersMoneyExpired,productsShipExpired)
    return text




if __name__ == "__main__":
    startTime = '{}'.format('2019-07-31')
    endTime = '{}'.format('2019-07-31')
    l = generate(startTime,endTime)
    with open("123.html",mode='w') as f:
        f.write(l)
    print(l)
