import logging
from tkinter import *
import socket
from urllib.parse import urlparse, urlsplit

logging.getLogger().setLevel(logging.DEBUG)

FILENAME = 'data'


class FileStorage:

    @classmethod
    def create_from_binary_data(cls, filename, data):
        with open(filename, 'wb') as file:
            file.write(data)


def pushbutton():
    try:
        inputValue = message_entryentr.get()
        url_data = urlparse(inputValue)
        logging.info(url_data)
        logging.info(url_data.hostname)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = url_data.hostname
        port = 80
        s.connect((host, port))
        s.send(b'GET / HTTP/1.1\r\n\r\n')
        data = b''
        while True:
            r = s.recv(1024)
            if not r:
                break
            data += r

        logging.info(f'[data] size: {len(data)}')
        s.close()

        FileStorage.create_from_binary_data(FILENAME, data)
    except BaseException:
        logging.exception("can't load")




root = Tk()
root.title("GUI на Python")
root.geometry("300x250")

message = StringVar()
message_entryentr = Label(text="ведите адресс:")
message_entryexit = Label(text="вывод данных:")

message_entryentr.grid(row=1, column=1, padx=5, pady=5)
message_entryexit.grid(row=10, column=2, padx=5, pady=5)

message_entryentr = Entry(textvariable=message)
message_entryentr.place(relx=.6, rely=.1, anchor="c")

message_entryexit = Entry()
message_entryexit.place(relx=.5, rely=.5, anchor="c", height=100, width=200, )

btn = Button(text="скачать", command=pushbutton)
btn.place(relx=.5, rely=.85, anchor="c", height=30, width=130, bordermode=OUTSIDE)

root.mainloop()
