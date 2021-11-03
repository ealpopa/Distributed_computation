#!/usr/bin/python
import socket;
import sys, time;
import threading, os;
from queue import Queue

#Implemented using 3 threads
#one thread for listening and accepting connections
#one thread for getting data
#one thread for sending data

NUMBER_OF_THREADS = 3;
JOB_NUM = [1, 2, 3];
HEX_CHARS = ['A', 'B', 'C', 'D', 'E', 'F'];
queue = Queue();

#connection queues
all_connections = [];
all_addresses = [];

def params():
#check and validate both parameters of the hypothesis
    global n_num;
    global hex_num;

    if len(sys.argv) < 3:
        n_num = int(input("Insert the n number (< 5 for faster computation): "));
        hex_num = input("Insert the hex stream(max. 6 hex chars for faster computation): ").upper();
        for char in hex_num:
            if char not in HEX_CHARS:
                print('\nInvalid argument. Please reinsert.\n');
                params(); 
    else:
        n_num = sys.argv[1]; 
        hex_num = sys.argv[2];

def socket_create():
    try:
        global host;
        global port
        global s;
        host = '127.0.0.1';
        port = 1800;
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0);
    except socket.error as msg:
        print("Socket creation error: " + str(msg));

def socket_bind():
    try:
        global host;
        global port
        global s;
        s.bind((host, port));
        s.listen(5);
        print('Waiting for client connections');
    except socket.error as msg:
        print("Socket binding error: " + str(msg));
        time.sleep(5);
        socket_bind();

def accept_connections():
    for c in all_connections:
        c.close();
    del all_connections[:];
    del all_addresses[:];
    while True:
        try:
            conn, addr = s.accept();
            conn.setblocking(1);
            all_connections.append(conn);
            all_addresses.append(addr);
            print("Connection client {} from {}\n".format(all_connections.index(conn), addr));
        except:
            print("Connection rejected");

def read_data():
#get info on client computation progress or final result found
    found = False;
    while not found:
        for id, conn in enumerate(all_connections):
            data = conn.recv(1024).decode();
            if "ok" in data:
                seed = data.split(',')[1];
                hash = data.split(',')[2];
                found = True;
                print('Final. Clientul {} found seed: {} for hash: {}\n'.format(id, seed, hash));
                print('Quit by pressing Ctrl+C.');
                for c in all_connections:
                    c.send('stop,{}'.format(id).encode());
                    c.close();
                break;
            else:
                print("Client {}, address {}: {}".format(id, all_addresses[id], data));
    sys.exit();
    return "Found";
    
def send_data():
#send the initial hypothesis data
    visited = [];
    while True:        
        for conn in all_connections:
            if (len(all_connections) > 1) and conn not in visited:
                conn.send("{},{},{}".format(all_connections.index(conn),n_num, hex_num).encode());
                visited.append(conn);

def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work);
        t.daemon = True;
        t.start();

def work():
    while True:
        x = queue.get();
        if x == 1:
            socket_create();
            socket_bind();
            accept_connections();
        if x == 2:
            send_data();
        if x == 3:
            if read_data() == "Found":
                break;
        queue.task_done();

def create_work():
    for x in JOB_NUM:
        queue.put(x);
    queue.join();

if __name__ == "__main__":
#launch program

    params();
    create_threads();
    create_work();
