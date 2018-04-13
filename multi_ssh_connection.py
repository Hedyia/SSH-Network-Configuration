import paramiko #SSH
import time #Second func
import sys #2 arg from OS
import re #check for string
from threading import Thread as TH #openmp


def open_ssh_connection(ip):
    try:
        user_file = sys.argv[1]
        cmd_file = sys.argv[2]

        selected_user_file = open(user_file, 'r')
        selected_user_file.seek(0)

        username = selected_user_file.readlines()[0].split(',')[0]
        selected_user_file.seek(0)
        password = selected_user_file.readlines()[0].split(',')[1].rstrip('\n')

        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        session.connect(ip, port=22, username=username, password=password)
        connection = session.invoke_shell()
        connection.send('terminal length 0\n')
        time.sleep(1)

        connection.send('\n')
        connection.send('enable\n')
        connection.send('py\n')
        time.sleep(1)
        connection.send('conf terminal\n')
        selected_cmd_file = open(cmd_file, 'r')
        selected_cmd_file.seek(0)
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(1)
        selected_cmd_file.close()
        selected_user_file.close()
        router_output = connection.recv(65535)
        if re.search(r'% Invalid input detected at', router_output):
            print ('* There was at least one IOS syntax error on device %s' % ip)
            print router_output + '\n'
        else:
            print ('\nDone for Device %s' % ip)
            print (router_output + '\n')
            session.close()
    except paramiko.AuthenticationException:
        print ('* Invalid username or password check your username file routers configuration')
        print ('* Closing progam')


def main():
    ip = ['192.168.1.201', '192.168.1.202', '192.168.1.203', '192.168.1.204', '192.168.1.205']
    threads = []

    for i in range(5):
        th = TH(target=open_ssh_connection, args=[ip[i]])
        th.start()
        threads.append(th)
    for i in range(5):
        th.join()


if __name__ == '__main__':
    main()
