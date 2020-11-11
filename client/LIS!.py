from tkinter import *
import threading
from tkinter import messagebox
import time
import socket
import select
from PIL import ImageGrab, Image, ImageTk
import pyaudio
import tkinter.scrolledtext as st

isascii = lambda s: len(s) == len(s.encode())
colors4 = ["gray40", "gray26", "gray30", "gray10", "files\\logo4.png"]
colors3 = ["sienna1", "sienna2", "sienna3", "sienna4", "files\\logo3.png"]
colors2 = ["DarkOliveGreen1", "DarkOliveGreen2", "DarkOliveGreen3", "DarkOliveGreen4", "files\\logo2.png"]
colors1 = ["LightSkyBlue1", "LightSkyBlue2", "LightSkyBlue3", "LightSkyBlue4", "files\\logo.png"]
colors = colors1


# DID - [login,register,forgot password(add emial send),search and next page, home,]


class LogInPage:

    def __init__(self, master):
        global colors
        master.geometry("300x500")
        master.resizable(0, 0)
        base = Frame(master)
        base.grid(row=0, column=0)
        self.b = base
        self.m = master
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=301, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="Welcome to L.I.S", background=colors[3], font=("Helvetica", 12),
              foreground="white").place(x=85)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=301, height=471)
        self.down_frame.grid(row=2, column=0)

        Label(self.down_frame, text="User Name", background=colors[0], font=("Helvetica", 10)).place(x=0, y=10)
        self.user_name = Entry(self.down_frame, width=30, borderwidth=2, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.user_name.place(x=72, y=10)
        Label(self.down_frame, text="Password", background=colors[0], font=("Helvetica", 10)).place(x=0, y=40)
        self.password = Entry(self.down_frame, width=30, borderwidth=2, relief=GROOVE, show="*"
                              , font=("Helvetica", 8, "bold"))
        self.password.place(x=72, y=40)

        log_in = Button(self.down_frame, text="Log In", command=lambda: self.login(base, master), borderwidth=1,
                        relief=GROOVE, width=10, background=colors[2])
        log_in.place(x=72, y=65)
        register_button = Button(self.down_frame, text="Register", command=lambda: self.move_page(base, master),
                                 borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        register_button.place(x=72, y=92)
        forgot = Button(self.down_frame, text="forgot your username or password?",
                        command=lambda: self.move_page(base, master, "new_password"), borderwidth=3, relief=FLAT,
                        width=26
                        , bg=colors[0], foreground="red")
        forgot.place(x=72, y=117)

        background = PhotoImage(file=colors[4])
        back = Label(self.down_frame, image=background, bg=colors[0])
        back.image = background
        back.place(x=30, y=180)
        self.user_name.bind("<Key>", self.focus1)
        self.password.bind("<Key>", self.focus2)

    def focus1(self, e):
        if e.char == "\r":
            self.password.focus()

    def focus2(self, e):
        if e.char == "\r":
            self.login(self.b, self.m)

    def login(self, base, master):
        global my_name
        # socket part -------------------------------------------------------------------
        data = "<LOG>/" + self.user_name.get() + "/" + self.password.get() + "/"
        client_socket.send(data.encode('utf-8'))
        data = client_socket.recv(4096)
        data = str(data)
        data = data[2:-1]
        # socket part -------------------------------------------------------------------

        if data == "log in":
            my_name = self.user_name.get()
            self.move_page(base, master, "main")
        else:
            self.user_name.focus()
            messagebox.showerror("error", data)
            self.user_name.delete(0, END)
            self.password.delete(0, END)

    def move_page(self, base, master, name="register"):
        base.destroy()
        if name == "register":
            Register(master)
        elif name == "main":
            MainPage(master)
            # main page
        elif name == "new_password":
            ForgotPassword(master)


class ForgotPassword:
    def __init__(self, master):
        global colors
        master.geometry("300x500")
        master.resizable(0, 0)
        base = Frame(master)
        base.grid(row=0, column=0)
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=301, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="Welcome to L.I.S", background=colors[3], font=("Helvetica", 12),
              foreground="white").place(x=85)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=301, height=471)
        self.down_frame.grid(row=2, column=0)

        back_button = Button(self.up_frame, text="<== back", command=lambda: self.move_page(base, master, "log_in"),
                             borderwidth=1, relief=FLAT, width=10, background=colors[3]
                             , font=("Helvetica", 9, "bold"), foreground="white")
        back_button.place(x=0, y=2)

        Label(self.down_frame, text="Enter your user name", background=colors[0],
              font=("Helvetica", 10)).place(x=100, y=10)
        Label(self.down_frame, text="User Name", background=colors[0], font=("Helvetica", 10)).place(x=0, y=40)
        self.user_name = Entry(self.down_frame, width=30, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.user_name.place(x=72, y=40)
        submit = Button(self.down_frame, text="Enter", command=lambda: self.send_email(), borderwidth=1,
                        relief=GROOVE, width=10, background=colors[2])
        submit.place(x=72, y=65)
        self.user_name.bind("<Key>", self.focus1)

    def focus1(self, e):
        if e.char == "\r":
            self.send_email()

    def send_email(self):
        # need to add send mail
        data = "<FOR>/" + self.user_name.get() + "/"
        client_socket.send(data.encode('utf-8'))
        data2 = client_socket.recv(5000)
        data2 = str(data2)
        data2 = data2[2:-1]
        print(data2)
        self.user_name.delete(0, END)
        if data2 == "not a real username":
            messagebox.showinfo("Information", "oops the username you entered does not exists")
        else:
            messagebox.showinfo("Information", "we sent you a mail ; )")

    def move_page(self, base, master, name="register"):
        base.destroy()
        if name == "log_in":
            LogInPage(master)


class Register:

    def __init__(self, master):
        global colors

        base = Frame(master)
        base.pack()
        master.geometry("300x500")
        base.grid(row=0, column=0)
        self.b = base
        self.m = master
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=301, height=30)
        self.up_frame.grid(row=0, column=0)

        Label(self.up_frame, text="Register to L.I.S", background=colors[3], font=("Helvetica", 12),
              foreground="white").place(x=85)

        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=301, height=471)
        self.down_frame.grid(row=2, column=0)

        Label(self.down_frame, text="User Name", background=colors[0], font=("Helvetica", 10)).place(x=0, y=15)
        self.user_name = Entry(self.down_frame, width=30, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.user_name.place(x=72, y=10)

        Label(self.down_frame, text="Email", background=colors[0], font=("Helvetica", 10)).place(x=0, y=45)
        self.email = Entry(self.down_frame, width=30, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.email.place(x=72, y=40)

        Label(self.down_frame, text="Password", background=colors[0], font=("Helvetica", 10)).place(x=0, y=75)
        self.password = Entry(self.down_frame, width=30, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold")
                              , show="*")
        self.password.place(x=72, y=70)

        Label(self.down_frame, text="Reenter \n Password", background=colors[0],
              font=("Helvetica", 10)).place(x=0, y=100)
        self.password_2 = Entry(self.down_frame, width=30, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold")
                                , show="*")
        self.password_2.place(x=72, y=110)

        submit_button = Button(self.down_frame, text="Submit", command=lambda: self.get_data(base, master),
                               borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        submit_button.place(x=72, y=140)

        back_button = Button(self.up_frame, text="<== back", command=lambda: self.move_page(base, master),
                             borderwidth=1, relief=FLAT, width=10, background=colors[3]
                             , font=("Helvetica", 9, "bold"), foreground="white")
        back_button.place(x=0, y=2)

        background = PhotoImage(file=colors[4])
        back = Label(self.down_frame, image=background, bg=colors[0])
        back.image = background
        back.place(x=-5, y=180)
        self.user_name.bind("<Key>", self.focus1)
        self.email.bind("<Key>", self.focus2)
        self.password.bind("<Key>", self.focus3)
        self.password_2.bind("<Key>", self.focus4)

    def focus1(self, e):
        if e.char == "\r":
            self.email.focus()

    def focus2(self, e):
        if e.char == "\r":
            self.password.focus()

    def focus3(self, e):
        if e.char == "\r":
            self.password_2.focus()

    def focus4(self, e):
        if e.char == "\r":
            self.get_data(self.b, self.m)

    def get_data(self, base, master, name="login"):
        user_name = self.user_name.get()
        email = self.email.get()
        password = self.password.get()
        password_2 = self.password_2.get()
        text = ""
        true_data = True
        # add socket stuff
        if len(user_name) >= 4:
            # add if exist
            pass
        else:
            text += "username length must be 4 letters or more\n "
            true_data = False
        if "@gmail.com" in email:
            # add if exist
            pass
        else:
            text += "email not valued\n"
            true_data = False
        if len(password) >= 4:
            if password == password_2:
                pass
            else:
                text += "passwords not same\n"
                true_data = False
        else:
            text += "password length must be 4 letters or more\n"
            true_data = False

        # socket part------------------------------------------------------
        if true_data:
            """
            <REG>/username/password/email/ - packet structure
            """
            data = "<REG>/" + user_name + "/" + password + "/" + email + "/"
            client_socket.send(data.encode('utf-8'))
            client_socket.send(data.encode('utf-8'))

            data = client_socket.recv(4096)
            data = str(data)
            data = data[2:-1]
            if data != "add":
                text += data
                true_data = False
        # socket part------------------------------------------------------

        if true_data:
            messagebox.showinfo("Information", "you have been registered please log in ")
            self.move_page(base, master, name)
        else:
            self.user_name.focus()
            messagebox.showerror("error", text)

    def move_page(self, base, master, name="login"):
        base.destroy()
        if name == "login":
            LogInPage(master)


class MainPage:
    def __init__(self, master):
        global colors
        self.current_p = 0
        self.results = []
        master.geometry("600x400")
        master.resizable(0, 0)
        base = Frame(master)
        base.grid(row=0, column=0)
        master.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=601, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="Main page of L.I.S    |", background=colors[3],
              font=("Helvetica", 12), foreground="white").place(x=85)
        log_out_button = Button(self.up_frame, text="<= Log out", command=lambda: self.move_page(base, master)
                                , borderwidth=1, relief=FLAT, width=10, background=colors[3],
                                font=("Helvetica", 9, "bold"), foreground="white")
        log_out_button.place(x=0, y=2)

        settings_button = Button(self.up_frame, text="Settings -O-   |"
                                 , command=lambda: self.move_page(base, master, "settings")
                                 , borderwidth=1, relief=FLAT, width=10, background=colors[3],
                                 font=("Helvetica", 9, "bold"), foreground="white")
        settings_button.place(x=440, y=2)

        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=601, height=471)
        self.down_frame.grid(row=2, column=0)
        self.search = Entry(self.down_frame, width=80, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.search.place(x=72, y=10)
        search_button = Button(self.down_frame, text="Search", command=lambda: self.search_line()
                               , borderwidth=2, relief=GROOVE, width=20, background=colors[2],
                               font=("Helvetica", 9, "bold"))
        search_button.place(x=72, y=35)

        create_button = Button(self.down_frame, text="Create", command=lambda: self.create_s(base, master)
                               , borderwidth=2, relief=GROOVE, width=20, background=colors[2],
                               font=("Helvetica", 9, "bold"))
        create_button.place(x=232, y=35)
        Label(self.down_frame, text="  ________________________________________________________________"
              , background=colors[0],
              font=("Helvetica", 12)).place(x=0, y=65)
        if True:
            self.r_1 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_1['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_1.place(x=72, y=120)
            self.r_2 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_2['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_2.place(x=72, y=145)
            self.r_3 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_3['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_3.place(x=72, y=170)
            self.r_4 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_4['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_4.place(x=72, y=195)
            self.r_5 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_5['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_5.place(x=72, y=220)
            self.r_6 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_6['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_6.place(x=72, y=245)
            self.r_7 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_7['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_7.place(x=72, y=270)
            self.r_8 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_8['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_8.place(x=72, y=295)
            self.r_9 = Button(self.down_frame, text="", anchor=W
                              , command=lambda: self.move_page(base, master, "stream", self.r_9['text'])
                              , borderwidth=1, relief=FLAT, width=60, background=colors[1],
                              font=("Helvetica", 9, "bold"))
            self.r_9.place(x=72, y=320)
        next_button = Button(self.down_frame, text="Next", command=lambda: self.next_page()
                             , borderwidth=2, relief=GROOVE, width=10, background=colors[2],
                             font=("Helvetica", 9, "bold"))
        next_button.place(x=510, y=320)
        self.lab = Label(self.down_frame, text="page:" + str(abs(self.current_p + 1)), background=colors[0],
                         font=("Helvetica", 12), foreground="red")
        self.lab.place(x=510, y=345)

    def create_s(self, base, master):
        s_name = self.search.get()
        if s_name != "" and isascii(s_name):
            u_name = my_name
            try:
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                port = get_free_tcp_port()
                data = "<CRT>/" + ip + "," + str(port) + "/" + s_name + "/" + u_name
                client_socket.send(data.encode('utf-8'))
                data2 = client_socket.recv(5000)
                print(data2)
                self.move_page(base, master, "maker", s_name + "-" + u_name, str(ip) + "/" + str(port))
            except:
                print("create problem try later")
        else:
            self.search.delete(0, END)

    def next_page(self):
        print(self.current_p + 1)
        if len(self.results) > 0:
            if self.current_p + 1 == len(self.results):
                self.current_p = -1

            self.current_p += 1
            self.show_search(self.current_p)


        else:
            self.current_p = 0
        self.lab.config(text="page:" + str(abs(self.current_p + 1)))

    def search_line(self):
        pages = [["", "", "", "", "", "", "", "", ""]]

        data = self.search.get()

        data = "<SER>/" + data + "/"
        client_socket.send(data.encode('utf-8'))
        data2 = client_socket.recv(5000)
        data2 = str(data2)
        data2 = data2[2:-1]
        data2 = data2.split("/")

        long = len(data2)
        for p in range(0, (long - 3) // 9):
            pages.append(["", "", "", "", "", "", "", "", ""])
        for i in range(1, long - 1):
            page = (i - 1) // 9
            pages[page][i - (9 * page) - 1] = data2[i]
        self.search.delete(0, END)

        self.results = pages

        self.show_search(0)

    def show_search(self, page):

        try:
            print(self.results[page])
            self.r_1['text'] = self.results[page][0]
            self.r_2['text'] = self.results[page][1]
            self.r_3['text'] = self.results[page][2]
            self.r_4['text'] = self.results[page][3]
            self.r_5['text'] = self.results[page][4]
            self.r_6['text'] = self.results[page][5]
            self.r_7['text'] = self.results[page][6]
            self.r_8['text'] = self.results[page][7]
            self.r_9['text'] = self.results[page][8]
        except:
            self.r_1['text'] = ""
            self.r_2['text'] = ""
            self.r_3['text'] = ""
            self.r_4['text'] = ""
            self.r_5['text'] = ""
            self.r_6['text'] = ""
            self.r_7['text'] = ""
            self.r_8['text'] = ""
            self.r_9['text'] = ""

    def move_page(self, base, master, name="login", s_name="none", ip=""):

        if name == "login":
            base.destroy()
            LogInPage(master)
        elif name == "settings":
            base.destroy()
            Settings(master)
        elif name == "stream":
            if s_name != '':
                base.destroy()
                Stream(master, s_name)
        elif name == "maker":
            base.destroy()
            StreamMaker(master, ip, s_name)
            # s_name as ip and port


class StreamMaker:

    def __init__(self, master, ip_port, s_name):
        global colors
        self.loop = True
        self.loop2 = True
        master.geometry("900x430")
        master.resizable(0, 0)
        base = Frame(master)
        base.grid(row=0, column=0)
        master.protocol("WM_DELETE_WINDOW", lambda: self.quit(base, master))

        ip_port = ip_port.split("/")
        self.ip = ip_port[0]
        self.port = ip_port[1]
        self.s_name = s_name

        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=901, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="L.I.S - enjoy watching the stream", background=colors[3], font=("Helvetica", 12),
              foreground="white").place(x=150)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=901, height=401)
        self.down_frame.grid(row=2, column=0)

        back_button = Button(self.up_frame, text="<== back", command=lambda: self.move_page(base, master),
                             borderwidth=1, relief=FLAT, width=10, background=colors[3]
                             , font=("Helvetica", 9, "bold"), foreground="white")
        back_button.place(x=0, y=2)

        self.screen = Canvas(self.down_frame, borderwidth=2, relief=FLAT, background=colors[3], width=650, height=320)
        self.screen.place(x=10, y=10)

        self.text = Entry(self.down_frame, width=60, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.text.place(x=10, y=340)
        submit_button = Button(self.down_frame, text="send-->", command=lambda: self.get_data(),
                               borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        submit_button.place(x=10, y=365)
        self.chat = st.ScrolledText(self.down_frame, borderwidth=1, relief=GROOVE, width=25, background=colors[2],
                                    height=23)
        self.chat.place(x=680, y=10)
        self.chat.bind("<Key>", lambda e: "break")

        self.server_chat = socket.socket()
        self.server_chat.bind((self.ip, int(self.port)))
        self.server_screen = socket.socket()
        self.server_screen.bind((self.ip, int(self.port) + 1))
        self.server_voice = socket.socket()
        self.server_voice.bind((self.ip, int(self.port) + 2))
        self.server_chat.listen(255)
        self.server_screen.listen(255)
        self.server_voice.listen(255)
        self.open_client_sockets = []
        self.open_client_sockets2 = []
        self.open_client_sockets3 = []

        HUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        frames = []
        WIDTH = 2
        self.p = pyaudio.PyAudio()
        try:
            self.stream = self.p.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)

            self.stream2 = self.p.open(format=self.p.get_format_from_width(WIDTH),
                                       channels=CHANNELS,
                                       rate=RATE,
                                       output=True,
                                       frames_per_buffer=CHUNK)
        except:
            self.stream = ""
            self.stream2 = ""
        threading.Thread(target=lambda: self.chat_server()).start()
        threading.Thread(target=lambda: self.screen_server()).start()
        threading.Thread(target=lambda: self.record_server()).start()
        threading.Thread(target=lambda: self.screen_show()).start()
        threading.Thread(target=lambda: self.record(CHUNK)).start()

    def record(self, chunk):

        while self.loop:
            try:
                data = self.stream.read(chunk)
                for conn in self.open_client_sockets3:
                    try:
                        conn.sendall(data)
                    except:
                        pass
                self.stream2.write(data)
            except:
                for conn in self.open_client_sockets3:
                    try:
                        conn.sendall("")
                    except:
                        pass
                try:
                    HUNK = 1024
                    FORMAT = pyaudio.paInt16
                    CHANNELS = 1
                    RATE = 44100
                    CHUNK = 1024
                    frames = []
                    WIDTH = 2
                    self.stream = self.p.open(format=FORMAT,
                                              channels=CHANNELS,
                                              rate=RATE,
                                              input=True,
                                              frames_per_buffer=CHUNK)

                    self.stream2 = self.p.open(format=self.p.get_format_from_width(WIDTH),
                                               channels=CHANNELS,
                                               rate=RATE,
                                               output=True,
                                               frames_per_buffer=CHUNK)
                except:
                    pass

    def record_server(self):
        data = "o"
        while self.loop:
            rlist, wlist, xlist = select.select([self.server_voice] + self.open_client_sockets3, [], [])
            for current_socket in rlist:
                if current_socket is self.server_voice:
                    try:
                        (new_socket, address) = self.server_voice.accept()
                        self.open_client_sockets3.append(new_socket)
                    except:
                        pass
                else:
                    try:
                        try:
                            data = current_socket.recv(4096)
                            data = str(data)
                            data = data[2:-1]
                        except ConnectionResetError:
                            self.open_client_sockets3.remove(current_socket)
                        finally:
                            pass
                        if data == "":
                            self.open_client_sockets3.remove(current_socket)
                            print("leave")
                        else:
                            pass
                    finally:
                        pass

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.server_voice.close()

    def screen_server(self):

        while self.loop:
            try:
                rlist, wlist, xlist = select.select([self.server_screen] + self.open_client_sockets2, [], [])
                for current_socket in rlist:
                    if current_socket is self.server_screen:
                        (new_socket, address) = self.server_screen.accept()
                        self.open_client_sockets2.append(new_socket)
                    else:
                        try:
                            data = current_socket.recv(4096)
                            data = str(data)
                            data = data[2:-1]
                        except ConnectionResetError:
                            self.open_client_sockets2.remove(current_socket)
                            print("leave")

                        if data == "":
                            self.open_client_sockets2.remove(current_socket)
                            print("leave")
            except:
                pass

    def screen_show(self):
        num = 0
        old_photo = 0
        while self.loop2:
            if num % 40 == 0:
                self.screen = Canvas(self.down_frame, borderwidth=2, relief=FLAT, background=colors[3], width=650,
                                     height=320)
                self.screen.place(x=10, y=10)
                try:
                    self.screen.create_image(325, 165, image=old_photo)
                except:
                    pass
                if num >= 1000:
                    num = 0
            im = ImageGrab.grab()
            im = im.resize((650, 320), Image.ANTIALIAS)
            im.save("files\\screen1.png", quality=1)
            im = open("files\\screen1.png", "rb")
            r_im = im.read()
            im.close()
            for i in self.open_client_sockets2:
                try:
                    i.sendall(r_im)
                except:
                    print("t")
            try:
                pilImage = Image.open("files\\screen1.png")
                image = ImageTk.PhotoImage(pilImage)
                old_photo = image
            except:
                print("l")
            try:
                self.screen.create_image(325, 165, image=image)
            except:
                print("o")
            num += 1
        else:
            print("e")

    def chat_server(self):
        while self.loop:
            try:
                rlist, wlist, xlist = select.select([self.server_chat] + self.open_client_sockets, [], [])
                for current_socket in rlist:
                    if current_socket is self.server_chat:
                        (new_socket, address) = self.server_chat.accept()
                        self.open_client_sockets.append(new_socket)
                    else:
                        try:
                            data = current_socket.recv(4096)
                            data = str(data)
                            data = data[2:-1]
                        except ConnectionResetError:
                            self.open_client_sockets.remove(current_socket)
                            print("leave")

                        if data == "":
                            self.open_client_sockets.remove(current_socket)
                            print("leave")
                        else:
                            self.chat.insert(END, data + "\n")
                            self.chat.yview(END)
                            threading.Thread(target=lambda: self.send_to_all(data)).start()
            except:
                pass

    def send_to_all(self, message):
        for i in self.open_client_sockets:
            i.send(message.encode('utf-8'))

    def get_data(self):
        if self.text.get() != "" and self.text.get().strip() != "" and isascii(self.text.get()):
            self.chat.insert(END, ">-" + self.text.get().rstrip() + "\n")
            self.send_to_all(">-" + self.text.get().rstrip())
            self.text.delete(0, END)
            self.chat.yview(END)
        else:
            self.text.delete(0, END)

    def move_page(self, base, master, name="main"):

        if name == "main":
            self.loop = False
            self.loop2 = False
            self.server_chat.close()
            self.server_screen.close()
            self.server_voice.close()
            time.sleep(0.2)
            data = "<RMV>/" + self.s_name + "/" + self.ip + "/" + self.port + "/"
            client_socket.send(data.encode('utf-8'))
            time.sleep(0.3)
            base.destroy()
            MainPage(master)

    def quit(self, base, master, name="main"):
        self.move_page(base, master, "main")


class Stream:

    def __init__(self, master, name):
        global colors
        global my_name
        self.loop = True
        master.geometry("900x430")
        master.resizable(0, 0)

        base = Frame(master)
        master.protocol("WM_DELETE_WINDOW", lambda: self.quit(base, master))
        self.bm = [base, master]
        base.grid(row=0, column=0)
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=901, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="L.I.S - enjoy watching the stream", background=colors[3], font=("Helvetica", 12),
              foreground="white").place(x=150)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=901, height=401)
        self.down_frame.grid(row=2, column=0)

        back_button = Button(self.up_frame, text="<== back", command=lambda: self.move_page(base, master),
                             borderwidth=1, relief=FLAT, width=10, background=colors[3]
                             , font=("Helvetica", 9, "bold"), foreground="white")
        back_button.place(x=0, y=2)

        self.screen = Canvas(self.down_frame, borderwidth=2, relief=FLAT, background=colors[3], width=650, height=320)
        self.screen.place(x=10, y=10)
        self.text = Entry(self.down_frame, width=60, borderwidth=3, relief=GROOVE, font=("Helvetica", 8, "bold"))
        self.text.place(x=10, y=340)
        submit_button = Button(self.down_frame, text="send-->", command=lambda: self.get_data(),
                               borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        submit_button.place(x=10, y=365)
        self.chat = st.ScrolledText(self.down_frame, borderwidth=1, relief=GROOVE, width=25, background=colors[2],
                                    height=23)
        self.chat.place(x=680, y=10)
        self.chat.bind("<Key>", lambda e: "break")

        data = "<NAME>/" + name + "/"
        client_socket.send(data.encode('utf-8'))
        data2 = client_socket.recv(5000)
        data2 = str(data2)
        data2 = data2[2:-1]
        data2 = data2.split("/")
        print(data2)

        self.client_chat = socket.socket()
        self.client_chat.connect((data2[0], int(data2[1])))
        self.client_screen = socket.socket()
        self.client_screen.connect((data2[0], int(data2[1]) + 1))
        self.client_record = socket.socket()
        self.client_record.connect((data2[0], int(data2[1]) + 2))

        CHUNK = 1024
        format1 = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        WIDTH = 2
        frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(WIDTH),
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

        threading.Thread(target=lambda: self.chat_client()).start()
        threading.Thread(target=lambda: self.screen_client()).start()
        threading.Thread(target=lambda: self.record_client(p, stream, frames)).start()

    def record_client(self, p, stream, frames):
        datas = self.client_record.recv(1024)

        while self.loop:
            stream.write(datas)
            try:
                datas = self.client_record.recv(1024)
            except:
                pass
        # stream.stop_stream()
        stream.close()
        p.terminate()

    def screen_client(self):
        num = 0
        old_photo = 0
        while self.loop:
            if num % 40 == 0:
                try:
                    self.screen = Canvas(self.down_frame, borderwidth=2, relief=FLAT, background=colors[3], width=650,
                                         height=320)
                    self.screen.place(x=10, y=10)
                except:
                    pass
                try:
                    self.screen.create_image(325, 165, image=old_photo)
                except:
                    pass
                if num >= 1000:
                    num = 0
            try:
                d = self.client_screen.recv(40960000)
                myfile = open("files\\screen.png", 'wb')
                myfile.write(d)
                try:
                    pilImage = Image.open("files\\screen.png")
                    image = ImageTk.PhotoImage(pilImage)
                    self.screen.create_image(325, 165, image=image)
                    old_photo = image
                except:
                    pass
            except:
                pass
            num += 1

    def chat_client(self):
        try:
            while self.loop:
                data = self.client_chat.recv(4096)
                data = str(data)
                data = data[2:-1]
                self.chat.insert(END, data + "\n")
                self.chat.yview(END)
        except:
            pass

    def get_data(self):
        try:
            if self.text.get() != "" and self.text.get().strip() != "" and isascii(self.text.get()):
                self.client_chat.send((my_name + ">-" + self.text.get().rstrip()).encode('utf-8'))
                self.text.delete(0, END)
            else:
                self.text.delete(0, END)
        except:
            self.move_page(self.bm[0], self.bm[1])

    def move_page(self, base, master, name="main"):
        base.destroy()
        if name == "main":
            try:
                self.client_chat.send(b"")
                self.client_screen.send(b"")
                self.client_record.send(b"")
            except:
                pass
            time.sleep(0.2)
            try:
                self.client_chat.close()
                self.client_screen.close()
                self.client_record.close()
            except:
                pass
            self.loop = False
            MainPage(master)

    def quit(self, base, master):
        self.move_page(base, master, "main")


class Settings:
    def __init__(self, master):
        global colors
        global colors1
        global colors2
        master.geometry("600x400")
        master.resizable(0, 0)
        base = Frame(master)
        base.grid(row=0, column=0)
        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=851, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="Settings - modify L.I.S ", background=colors[3], font=("Helvetica", 12)
              , foreground="white").place(x=150)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=851, height=401)
        self.down_frame.grid(row=2, column=0)

        back_button = Button(self.up_frame, text="<== back", command=lambda: self.move_page(base, master),
                             borderwidth=1, relief=FLAT, width=10, background=colors[3]
                             , font=("Helvetica", 9, "bold"), foreground="white")
        back_button.place(x=0, y=2)

        Label(self.down_frame, text="Change colors -", background=colors[0], font=("Helvetica", 12)).place(x=10, y=20)

        submit_button = Button(self.down_frame, text="Sky Blue", command=lambda: self.color_change(base, master, "1"),
                               borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        submit_button.place(x=10, y=50)
        submit_button = Button(self.down_frame, text="Olive", command=lambda: self.color_change(base, master, "2"),
                               borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        submit_button.place(x=90, y=50)
        submit_button = Button(self.down_frame, text="Sienna", command=lambda: self.color_change(base, master, "3"),
                               borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        submit_button.place(x=170, y=50)
        submit_button = Button(self.down_frame, text="Night Mode", command=lambda: self.color_change(base, master, "4"),
                               borderwidth=1, relief=GROOVE, width=10, background=colors[2])
        submit_button.place(x=250, y=50)

    def color_change(self, base, master, color, name="refresh"):
        global colors
        global colors1
        global colors2
        global colors3
        global colors4
        if color == "1":
            colors = colors1
        elif color == "2":
            colors = colors2
        elif color == "3":
            colors = colors3
        elif color == "4":
            colors = colors4
        self.move_page(base, master, name)

    def move_page(self, base, master, name="main"):
        base.destroy()
        if name == "main":
            MainPage(master)
        if name == "refresh":
            Settings(master)


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


my_name = "admin"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_server = input("please enter the server ip:")
port_server = input("please enter the server port:")
run_prog = True
try:
    client_socket.connect((ip_server, int(port_server)))
except:
    print("no connection")
    run_prog = False

if run_prog:
    root = Tk()
    root.wm_iconbitmap('files\\logo.ico')
    root.wm_title('L.I.S - live stream app')
    LogInPage(root)
    root.mainloop()
# threading.Thread(target=lambda:).start()\
"""
as
"""
