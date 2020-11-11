import socket
import select
import smtplib
import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8080))
server_socket.listen(255)
open_client_sockets = []
live_now = []


def register(name, password, email):
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    u = name
    p = password
    e = email
    for line in data:
        if line[0] == name:
            return False
    c.execute('INSERT INTO users (username, password, email) VALUES(? ,? ,? )', (u, p, e))
    conn.commit()
    return True


def log_in(name, password):
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    for line in data:
        if line[0] == name:
            if line[1] == password:
                return True
            return False
    return False


def forgot(name):
    c.execute("SELECT * FROM users")
    data = c.fetchall()

    for line in data:
        if line[0] == name:
            return line[2], line[1]

    return "Not real username", "no you cant get it"


def searching(search):
    search_list = "data/"
    for live in live_now:
        if search in live[0]:
            search_list += (live[0]+"/")

    return search_list


def create(s_name, u_name, ip, port):
    global live_now
    live_now += [[s_name+"-"+u_name, 0, ip, port]]

def enter(name):
    global  live_now
    i = 0
    for live in live_now:
        if name == live[0]:
            return live_now[i][2], live_now[i][3]
        i += 1
while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, [], [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
        else:
            try:
                try:
                    data = current_socket.recv(4096)
                    data = str(data)
                    data = data[2:-1]
                except ConnectionResetError:
                    open_client_sockets.remove(current_socket)
                finally:
                    pass
                if data == "":
                    open_client_sockets.remove(current_socket)
                    print("leave")
                else:
                    try:
                        data = data.split("/")
                    except:
                        pass
                    if data[0] == "<REG>":
                        """
                        <REG>/username/password/email/ - packet structure
                        """
                        if register(data[1], data[2], data[3]):
                            current_socket.send(b"add")
                        else:
                            current_socket.send(b"username already taken")
                    elif data[0] == "<LOG>":
                        """
                        <LOG>/username/password/ - packet structure
                        """
                        if log_in(data[1], data[2]):
                            current_socket.send(b"log in")
                        else:
                            current_socket.send(b"username or password is wrong")
                    elif data[0] == "<FOR>":
                        """
                        <FOR>/username/ - packet structure
                        """
                        mails,password = forgot(data[1])
                        if "@" not in mails:
                            current_socket.send(b"not a real username")

                        else:
                            admin = "lis.help.you@gmail.com"
                            mail = smtplib.SMTP('64.233.184.108', 587)
                            mail.ehlo()
                            mail.starttls()
                            mail.login(admin, "ofek1234")
                            mail.sendmail(admin,mails, """
                            Hello there from LIS!
                            We heard you forgot your password
                            your password is """ + password)
                            mail.close()
                            current_socket.send(b"we sent you a mail")
                    elif data[0] == "<SER>":
                        """
                        <SER>/search/ - packet structure
                        """
                        current_socket.send(searching(data[1]).encode('utf-8'))
                    elif data[0] == "<CRT>":
                        """
                        <CRT>/ip/s_name/u_name - packet structure
                        """
                        ip_port = data[1]
                        ip = ip_port.split(",")[0]
                        port = ip_port.split(",")[1]
                        s_name = data[2]
                        u_name = data[3]
                        create(s_name, u_name, ip, port)
                        print(live_now)
                        current_socket.send(("okey "+str(ip)+" "+str(port)+" "+s_name+" "+u_name).encode('utf-8'))
                    elif data[0] == "<NAME>":
                        ip1, port1 = enter(data[1])
                        current_socket.send((ip1+"/"+port1).encode('utf-8'))
                    elif data[0]== "<RMV>":
                        live_now.remove([data[1], 0, data[2], data[3]])
                        print(live_now)
            except:
                pass
c.close()
conn.close()