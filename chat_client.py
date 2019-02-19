from socket import * 
import os,sys 

# 发送消息
def send_msg(s,name,addr):
    while True:
        text=input('发言：')
        if text == 'quit':
            msg='Q '+name
            s.sendto(msg.encode(),addr)
            sys.exit('退出聊天室')
        msg='C %s %s'%(name,text)
        s.sendto(msg.encode(),addr)

# 接收消息
def recv_msg(s):
    while True:
        data,addr=s.recvfrom(2048)
        # 接收服务器发来的退出标志后退出该进程
        if data.decode() =='EXIT':
            sys.exit(0)
        print(data.decode()+'\n发言：',end='')

# 创建套接字
def main():
    # 从命令行输入服务器地址
    if len(sys.argv)<3:
        print("argv is error")
        return 
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    # 创建套接字
    s=socket(AF_INET,SOCK_DGRAM)
    while True:
        name=input("请输入姓名:")
        msg="L "+name
        # 发送给服务端
        s.sendto(msg.encode(),ADDR)
        # 等待回应
        data,addr=s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    # 创建父子进程
    pid = os.fork()
    if pid < 0:
        sys.exit('创建进程失败')
    elif pid == 0:
        send_msg(s,name,ADDR)
    else:
        recv_msg(s)

if __name__=="__main__":
    main()