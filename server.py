from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = '192.168.29.220'
PORT = 7560
ADDRESS = (HOST, PORT)
MAX_CONNECTIONS = 5
BUFFER_SIZE = 512

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)
QUIT_CMD = '{/%quit%disconnect_now%/}'
conn_clients = []


def send_to_clients(msg, name, except_client):
    """
    Send message to every client except the one who sent it
    :param except_client: the client who sent the message
    :param msg: bytes['utf8']
    :param name: str
    :return: None
    """
    for client in conn_clients:
        if client != except_client:
            client.send(bytes(name, "utf8") + msg)


def handle_clients(client):
    """
    handles each client connected to the server
    :param client: Client
    :return: None
    """
    name = client.recv(BUFFER_SIZE).decode('utf8')

    msg = bytes(f'{name} has joined the chat!', 'utf8')
    send_to_clients(msg, '', client)  # send_to_clients welcome message
    while True:
        try:
            msg = client.recv(BUFFER_SIZE)
            if msg == bytes(QUIT_CMD, "utf8"):
                client.close()
                conn_clients.remove(client)
                send_to_clients(bytes(f"{name} has left the chat", 'utf8'), "", client)
                print(f"{name} disconnected at {datetime.now().strftime('%H:%M:%S')}")
                break
            else:
                print(f'{name}: ', msg.decode("utf8"))
                send_to_clients(msg, name + ": ", client)

        except Exception as e:
            print("ERROR: ", e)
            break


def wait_for_connection(server):
    f"""
    waits for a maximum of {MAX_CONNECTIONS} clients to join
    to the server
    :param server: Socket
    :return: None
    """
    running = True
    while running:
        try:
            client, address = server.accept()
            conn_clients.append(client)
            print(f"{address} connected to the server at {datetime.now().strftime('%H:%M:%S')}")
            Thread(target=handle_clients, args=(client,)).start()
        except Exception as e:
            print("ERROR: ", e)
            running = False
    print("ERROR: SERVER CRASHED")


if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS)  # listen for 5 connections
    print("[CONNECTING] Waiting for connections ...")
    start_thread = Thread(target=wait_for_connection, args=(SERVER,))
    start_thread.start()
    start_thread.join()
    SERVER.close()
