import threading
import inspect
import ctypes 

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    try:
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble, 
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except SystemExit:
        pass
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

# ——————————————————————————————————————————————————————————————————————————————————————————
# 以上代码来自https://www.cnblogs.com/rainduck/archive/2013/03/29/2989810.html,用于结束线程。
# 以下代码为作者自作。
# ——————————————————————————————————————————————————————————————————————————————————————————

import socket,threading
server=socket.socket()
server.bind(('192.168.0.101',25565))
server.listen(2) #监听客户以及设置监听的数量，如果想要更改可进入聊天服务器的客户的数量，直接更改此数字参数即可。
chat_record=open('D:/chat_record.txt','a')
chat_record.close()
client_list=[]
thread_list=[]
conn_list=[]
def client(): #定义用于接收客户信息的函数。
    conn=conn_list[0]
    while True:
        try:
            message=conn.recv(1024*1024*1024).decode('utf-8') #接收客户传来的信息。
            print(message)
            chat_record=open('D:/chat_record.txt','a') #录入聊天记录。
            chat_record.write(message+'\n')
            chat_record.close()
            for client_conn in client_list: #把新接收的信息发送给已进入的客户。
                client_conn.send(message.encode('utf-8'))
        except ConnectionResetError: #这是当客户主动断开连接时会产生的错误。
            conn_num=client_list.index(conn) #取conn在clien_list中的位置，是为了在下面的thread_list中取到这个conn所对应的thread，以用于停止进程。
            client_list.remove(conn)
            thread=thread_list[conn_num] #取出对应的thread。
            del thread_list[thread] #删除线程列表里对应的thread.
            stop_thread(thread) #结束此线程。
            break
        except ConnectionAbortedError: #这是当客户主动断开连接时会产生的错误。（这是客户主动断开连接时可能产生的第二个错误）
            conn_num=client_list.index(conn) #取conn在clien_list中的位置，是为了在下面的thread_list中取到这个conn所对应的thread，以用于停止进程。
            client_list.remove(conn)
            thread=thread_list[conn_num] #取出对应的thread。
            del thread_list[thread] #删除线程列表里对应的thread。
            stop_thread(thread) #结束此线程。
            break
while True:
    conn,address=server.accept() #响应连接的客户。（在客户未连接时会一直等待）
    client_list.append(conn) #把新进入的客户添加进客户列表里。
    if len(conn_list)==0:
        conn_list.append(conn) #把conn装进列表里是为了能在client函数里使用conn。（因为conn的一个不可迭代的socket对象，不能作为参数直接传导进线程的执行函数里）
    else:
        conn_list[0]=conn
    conn.send(('——连接成功——'+'\n').encode('utf-8'))
    chat_record=open('D:/chat_record.txt','r') #导入之前的聊天记录。
    conn.send((chat_record.read()+'\n').encode('utf-8')) #把之前的聊天记录发送给客户。
    chat_record.close()
    thread_list.append(threading.Thread(target=client)) #新建线程用于接收客户发送来的信息，并把此线程加入到线程列表里。
    thread_list[(len(thread_list)-1)].start() #开始运行线程
server.close()
