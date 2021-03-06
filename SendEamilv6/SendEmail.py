import tkinter
import tkinter.messagebox
from tkinter import ttk
import threading
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from GenerateSummeryForDay import generate
from GenerateSummeryForWeek import generateByWeek
import schedule
import time


root = tkinter.Tk()
root.geometry('800x600+400+150')
root.title('发送报表')
root.resizable(0,0)


lableFrom=tkinter.Label(root,text='发件人邮箱:',justify=tkinter.RIGHT,width=80)
lableFrom.place(x=20,y=40,width=80,height=20)
varmailbox=tkinter.StringVar(root,value='')
entrymailbox=tkinter.Entry(root,width=120,textvariable=varmailbox)
entrymailbox.place(x=120,y=30,width=200,height=40)



lablePwd=tkinter.Label(root,text='邮箱密码:',justify=tkinter.RIGHT,width=80)
lablePwd.place(x=20,y=90,width=80,height=20)
varPwd=tkinter.StringVar(root,value='')
entryPwd=tkinter.Entry(root,show='*',width=120,textvariable=varPwd)
entryPwd.place(x=120,y=80,width=200,height=40)


lableTo=tkinter.Label(root,text='收件人邮箱:',justify=tkinter.RIGHT,width=80)
lableTo.place(x=20,y=140,width=80,height=20)
varmailbox1=tkinter.StringVar(root,value='')
entrymailbox1=tkinter.Entry(root,width=120,textvariable=varmailbox1)
entrymailbox1.place(x=120,y=130,width=200,height=40)

lableStart=tkinter.Label(root,text='开始时间:',justify=tkinter.RIGHT,width=80)
lableStart.place(x=420,y=40,width=80,height=20)
varStart=tkinter.StringVar(root,value='')
entryStart=tkinter.Entry(root,width=120,textvariable=varStart)
entryStart.place(x=520,y=30,width=200,height=40)


lableEnd=tkinter.Label(root,text='结束时间:',justify=tkinter.RIGHT,width=80)
lableEnd.place(x=420,y=140,width=80,height=20)
varEnd=tkinter.StringVar(root,value='')
entryEnd=tkinter.Entry(root,width=120,textvariable=varEnd)
entryEnd.place(x=520,y=130,width=200,height=40)


lableEveryDay=tkinter.Label(root,text='每日发送时间设置',justify=tkinter.LEFT,width=80,font='10')
lableEveryDay.place(x=80,y=340,width=250,height=20)

lableTime = tkinter.Label(root,text='如:07:00:',justify=tkinter.LEFT,width=200)
lableTime.place(x=10,y=390,width=80,height=20)
varTime=tkinter.StringVar(root,value='')
entryTime=tkinter.Entry(root,width=120,textvariable=varTime)
entryTime.place(x=120,y=380,width=200,height=40)


lableEveryDay=tkinter.Label(root,text='每周发送时间设置',justify=tkinter.CENTER,width=80,font='10')
lableEveryDay.place(x=450,y=340,width=250,height=20)

lableWeekTime = tkinter.Label(root,text='如:19:00:',justify=tkinter.LEFT,width=80)
lableWeekTime.place(x=410,y=390,width=80,height=20)
varWeekTime=tkinter.StringVar(root,value='')
entryWeekTime=tkinter.Entry(root,width=120,textvariable=varWeekTime)
entryWeekTime.place(x=520,y=380,width=200,height=40)

try:
    filename = 'info.txt'
    with open(filename,'r') as fp:
        mailFrom, pwd, mailTo = fp.read().strip().split(',')
    varmailbox.set(mailFrom)
    varPwd.set(pwd)
    varmailbox1.set(mailTo)
except:
    pass


def thread_it(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()

    
    
def send(flag,mailbox,pwd,ToMailBoxes):
    '''
    发送邮件
    '''
    
    today = datetime.date.today()


    ToMailBoxesList = ToMailBoxes.split(';')
    try:   
        if flag==1: #1为每天发送，2为每周发送，3为每月发送，4为手动自定义发送
            
            startTime = '{}'.format(today)
            endTime = '{}'.format(today)
            time = '{} 至 {}'.format(startTime,endTime)
            text = generate(startTime,endTime)
        elif flag==2:
            sunday = datetime.date.today()
            one_day = datetime.timedelta(days=1)
            while sunday.weekday() != 6:#找到本周周天
                sunday += one_day
            startTime = '{} 00:00:00'.format(sunday)
            endTime = '{} 23:59:59'.format(sunday)
            startTime = datetime.datetime.strptime(startTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(days=7,hours=8)#间隔一周
            endTime = datetime.datetime.strptime(endTime,'%Y-%m-%d  %H:%M:%S')-datetime.timedelta(hours=8)
            time = '{} 至 {}'.format(startTime,endTime)
            text = generateByWeek(startTime,endTime)
        elif flag==3:
            pass
        elif flag==4:
            startTime = entryStart.get()
            endTime = entryEnd.get()
            time = '{} 至 {}'.format(startTime,endTime)
            text = generate(startTime,endTime)
        msg = MIMEText(text, 'html', 'utf-8')
        msg['From'] = formataddr(["admin", mailbox])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["boss", ToMailBoxes])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "{}-报表".format(time)  # 邮件的主题
        server = smtplib.SMTP("smtp.126.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(mailbox, pwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(mailbox, ToMailBoxesList, msg.as_string())
        server.quit()
        tkinter.messagebox.showinfo(title='报告',message='发送成功...')
    except Exception:
        tkinter.messagebox.showinfo(title='报告',message='发送失败...')


def WriteInfo():
    '''
    保存邮箱、密码信息
    '''
    mailbox = entrymailbox.get()
    pwd = entryPwd.get()
    ToMailBoxes = entrymailbox1.get()
    try:
        filename = 'info.txt'
        with open(filename, 'w') as f:
            f.write(','.join((mailbox,pwd,ToMailBoxes)))
        tkinter.messagebox.showinfo(title='报告',message='保存信息成功...')
    except:
        tkinter.messagebox.showinfo(title='报告',message='保存信息失败...')

    


def SendOnTime():
    '''
    根据手工设定的时间发送邮件
    '''
    
    try:
        filename = 'info.txt'
        with open(filename,'r') as fp:
            mailFrom, pwd, mailTo = fp.read().strip().split(',')
    except:
        pass
    send(4,mailFrom,pwd,mailTo)



def cancel():
    varmailbox.set('')
    varmailbox1.set('')
    varPwd.set('')


def SendEmailEveryDay():
    '''
    工作日发送邮件
    '''
    Time = entryTime.get()
    try:
        filename = 'info.txt'
        with open(filename,'r') as fp:
            mailFrom, pwd, mailTo = fp.read().strip().split(',')
    except:
        pass
    schedule.every().day.at(Time).do(send,1, mailFrom, pwd, mailTo)
    while True:
        schedule.run_pending()
        time.sleep(1)

def SendEmailEveryWeek():
    '''
    每周发送邮件
    '''
    Time = entryWeekTime.get()   
    try:
        filename = 'info.txt'
        with open(filename,'r') as fp:
            mailFrom, pwd, mailTo = fp.read().strip().split(',')
    except:
        pass
    schedule.every().sunday.at(Time).do(send,2, mailFrom, pwd, mailTo)
    while True:
        schedule.run_pending()
        time.sleep(1)



    

buttonOk=tkinter.Button(root,text='确认',command=lambda:thread_it(WriteInfo))
buttonOk.place(x=100,y=200,width=70,height=40)


buttonCancel = tkinter.Button(root, text='重置', command=cancel)
buttonCancel.place(x=200, y=200, width=80, height=40)

buttonSend=tkinter.Button(root,text='发送',command=lambda:thread_it(SendOnTime))
buttonSend.place(x=500,y=200,width=200,height=40)


buttonTime=tkinter.Button(root,text='保存',command=lambda:thread_it(SendEmailEveryDay))
buttonTime.place(x=80,y=500,width=200,height=40)

buttonWeekTime=tkinter.Button(root,text='保存',command=lambda:thread_it(SendEmailEveryWeek))
buttonWeekTime.place(x=480,y=500,width=200,height=40)




sh = ttk.Separator(root, orient=tkinter.HORIZONTAL)
sh.grid(row=2,column=1,columnspan=3,sticky="we")
 
sv = ttk.Separator(root, orient=tkinter.VERTICAL)
sv.grid(row=1,column=2,rowspan=3,sticky="ns")
 
root.columnconfigure(1,weight=1)
root.rowconfigure(1,weight=1)
root.columnconfigure(3,weight=1)
root.rowconfigure(3,weight=1)

root.mainloop()