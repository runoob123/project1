from socket import *
import sys
import getpass

#创建网络连接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    # 创建套接字
    s = socket()

    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return

    while True:
        print('''
        =============Welcome=============
        --  1.注册    2.登录     3.退出  --
        =================================
        ''')
        try:
            cmd = int(input("请输入命令>>"))
        except Exception as e:
            print("命令输入错误")
            continue

        if cmd not in [1,2,3]:
            print("请输入正确的命令:")
            sys.stdin.flush() #清除缓存
            continue
        elif cmd == 1:
            r = do_register(s)
            if r == 0:
                print("注册成功")
            elif r == 1:
                print("用户存在")
            else:
                print("注册失败")
        elif cmd == 2:
            name = do_login(s)
            if name:
                print("登陆成功")
                login(s,name)
            else:
                print("用户名或密码不正确")
        elif cmd == 3:
            s.send(b'E')
            sys.exit("谢谢使用")

def do_register(s):
    while True:
        name = input("用户名：")
        passwd = getpass.getpass("输入密码：")
        passwd1 = getpass.getpass("确认密码：")

        if (' 'in name ) or (' 'in passwd):
            print("用户名或密码不能有空格")
            continue
        if passwd1 != passwd:
            print("两次输入密码不一致")
            continue

        msg = 'R {} {}'.format(name,passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return 0
        elif data == 'EXISTS':
            return 1
        else:
            return 2

def do_login(s):
    name = input("用户名:")
    passwd = getpass.getpass("输入密码：")
    msg = 'L {} {}'.format(name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()

    if data == 'OK':
        return name
    else:
        return

def login(s,name):
    while True:
        print('''
        =================查询界面===============
        -- 1.查询      2.历史记录      3.退出  --
        =======================================
        ''')
        try:
            cmd = int(input("请输入命令>>"))
        except Exception as e:
            print("命令错误")
            continue

        if cmd not in [1,2,3]:
            print("请输入正确的命令")
            sys.stdin.flush() # 清除缓存
            continue
        elif cmd == 1:
            do_query(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            return


def do_query(s,name):
    while True:
        word = input("请输入单词：")
        if word == "##":
            break
        msg = 'Q {} {}'.format(name,word)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print("没有查到该单词")


def do_hist(s,name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print("没有历史记录")


if __name__ == '__main__':
    main()

















































