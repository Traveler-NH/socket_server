import wx,socket,threading
client=socket.socket()
client.connect(('192.168.0.101',25565))
def send(none): #定义发送信息的函数。
    client.send(('客户：'+textctrl_send.Value).encode('utf-8'))
    textctrl_send.Value=''
def recv(): #定义函数给子线程接收信息。
    while True:
        textctrl_message.write(client.recv(1024*1024*1024).decode('utf-8')+'\n') #把接收到的信息加入到文本框里。
app=wx.App(False)
frame=wx.Frame(parent=None,id=wx.ID_ANY,title='client',size=(800,500))
frame.Centre() #使框架位居屏幕中间。
frame.SetMaxSize((800,500)) #固定框架的大小，使之无法拉伸和最大化，但可以收缩和最小化。
button_send=wx.Button(parent=frame,id=1,label='发送',pos=(660,410),size=(90,40),style=0)
textctrl_send=wx.TextCtrl(parent=frame,id=2,pos=(5,240),size=(780,160),style=wx.TE_MULTILINE)
textctrl_message=wx.TextCtrl(parent=frame,id=2,pos=(5,0),size=(780,220),style=wx.TE_MULTILINE)
button_send.Bind(event=wx.EVT_BUTTON,handler=send)
frame.Show(True) #显示框架
recv=threading.Thread(target=recv)
recv.start()
app.MainLoop()
