from socket import AF_INET, socket, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread


class Client:
    """
    for communication with the server
    """
    HOST = gethostbyname(gethostname())
    PORT = 7560
    ADDRESS = (HOST, PORT)
    BUFFER_SIZE = 512
    __QUIT_CMD = '{/%quit%disconnect_now%/}'

    def __init__(self, name, chat_box):
        """
        Initialize object and send name to server
        :param name: str
        """
        self.num_of_msg = 0
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDRESS)
        self.chat_box = chat_box
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_messages(name)

    def receive_messages(self):
        """
        receive messages from the server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFER_SIZE).decode()
                self.num_of_msg += 1
                placing = float(self.num_of_msg)
                msg = msg + '\n'
                self.chat_box.config(state='normal')
                self.chat_box.insert(placing, msg, ('left_align',))
                self.chat_box.config(state='disabled')
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_messages(self, msg):
        """
        send messages to the server
        :param msg: str
        :return: None
        """
        self.client_socket.send(bytes(msg, 'utf8'))
        if msg.__eq__(self.__QUIT_CMD):
            self.client_socket.close()

    def disconnect(self):
        self.send_messages(self.__QUIT_CMD)
