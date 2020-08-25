# socket_server_and_client


## socket_server.py

这是一个用socket模块制作的网络通信程序服务端，采用多线程的方式来接收信息并把信息转发给所有连接到服务端的客户，从而实现实时通信的目的。

因为使用的是多线程，所以可以实现多人实时通信，避免了被另一个客户阻塞了套接字而导致信息无法被服务端实时接收。

当有新的客户连接到服务端时，服务端会立即响应，把该客户的套接字加入到客户列表```client_list```中，再把之前的聊天记录发送给客户，然后把该客户的套接字传进用于接收该客户信息的线程里的conn变量里。
在该客户的套接字加入到客户列表后，程序随即创建一个线程，并把此线程存进线程列表```thread_list```里，然后开始运行线程。

当客户主动断开连接时，服务端会产生相应的错误，用```try: except: ```语句可以处理错误——根据该线程的conn变量确定该客户的套接字在客户列表中的位置，将其从客户列表中删除，用于接收该客户信息的线程也从线程列表中删除并结束线程（因为用于接收该客户信息的线程是紧随着该客户的套接字加入客户列表后加入线程列表的，所以，其线程在线程列表中的位置与其套接字在客户列表中的位置是相同的。即获取了该客户的套接字在客户列表中的位置就等于获取了其线程在线程列表中的位置。）。这样，客户断开连接时就能把该客户所占用的服务端的资源清除。

当服务端接收到客户的信息时，会立即把信息存入到聊天记录文件```chat_recode.txt```中。

在此声明，用于结束线程的函数来自```https://www.cnblogs.com/rainduck/archive/2013/03/29/2989810.html```提供的源码。

## wxpython_socket_client.py

这个是网络通信程序客户端，用了wxpython来制作GUI，两个文本框和一个按钮可简单完成发送输入的信息和接收显示接收的信息（上面的编辑框用于接收，下面的用于输入信息）

依然采用socket模块进行通信。在创建好所有组件和绑定按钮事件后，新建一个线程用于接收信息，接收到的信息会立即加入到对应的文本框中。
