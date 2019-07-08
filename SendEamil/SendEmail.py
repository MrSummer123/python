import tkinter
import tkinter.messagebox
import threading
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from GenerateText import generate


root = tkinter.Tk()
root.geometry('400x300+500+200')
root.title('发送报表')
root.resizable(0,0)


lablePwd=tkinter.Label(root,text='发件人邮箱:',justify=tkinter.RIGHT,width=80)
lablePwd.place(x=20,y=40,width=80,height=20)
varmailbox=tkinter.StringVar(root,value='')
entrymailbox=tkinter.Entry(root,width=120,textvariable=varmailbox)
entrymailbox.place(x=120,y=30,width=200,height=40)



lablePwd=tkinter.Label(root,text='邮箱密码:',justify=tkinter.RIGHT,width=80)
lablePwd.place(x=20,y=90,width=80,height=20)
varPwd=tkinter.StringVar(root,value='')
entryPwd=tkinter.Entry(root,show='*',width=120,textvariable=varPwd)
entryPwd.place(x=120,y=80,width=200,height=40)


lablePwd=tkinter.Label(root,text='收件人邮箱:',justify=tkinter.RIGHT,width=80)
lablePwd.place(x=20,y=140,width=80,height=20)
varmailbox1=tkinter.StringVar(root,value='')
entrymailbox1=tkinter.Entry(root,width=120,textvariable=varmailbox1)
entrymailbox1.place(x=120,y=130,width=200,height=40)


def thread_it(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()

    
    
def send():
    mailbox = entrymailbox.get()
    pwd = entryPwd.get()
    mailbox1 = entrymailbox1.get()
    try: 
        # time = str(datetime.date.today())
        time = '2018-11-08'
        text = generate(time)
        msg = MIMEText(text, 'html', 'utf-8')
        msg['From'] = formataddr(["admin", mailbox])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["admin", mailbox1])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "{}-报表".format(time)  # 邮件的主题
        server = smtplib.SMTP("smtp.126.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(mailbox, pwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(mailbox, [mailbox1, ], msg.as_string())
        server.quit()
        tkinter.messagebox.showinfo(title='报告',message='发送成功...')
    except Exception:
        tkinter.messagebox.showinfo(title='报告',message='发送失败...')

def cancel():
    varmailbox.set('')
    varmailbox1.set('')
    varPwd.set('')
    

buttonOk=tkinter.Button(root,text='确认',command=lambda:thread_it(send))
buttonOk.place(x=100,y=200,width=70,height=40)


buttonCancel = tkinter.Button(root, text='重置', command=cancel)
buttonCancel.place(x=200, y=200, width=80, height=40)



root.mainloop()

