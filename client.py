#!/usr/bin/python
import socket;
import hashlib;
import sys;
import threading, os;
from queue import Queue

#implemented using two dedicated threads
#one thread for client-server comms
#one thread for calculations

NUMBER_OF_THREADS = 2;
JOB_NUM = [1, 2];

queue = Queue();

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0);
##host = '127.0.0.1';

if len(sys.argv) < 2:
    print("\nYou forgot to input argument (server IP address)\n");

host = sys.argv[1];
port = 1800;

try:
    s.connect((host, port));
    print("You are connected to the server");
except socket.error as msg:
        print("Could not connect to server");

#receiving and parsing hypothesis
#id client, n, hex stream
info = s.recv(9).decode();
client_id = int(info.split(',')[0]);
n_num = int(info.split(',')[1]);
hex_num = info.split(',')[2];

print('Your are Client {}. We are looking for n = {}, initial string = {}'.format(client_id, n_num, hex_num));

def compute():
#do the calculations
    count = 0;
    while True:
        seed = hex(count);
        seed_hex = seed + hex_num;
        result = hashlib.md5(seed_hex.encode());
        res_hex = result.hexdigest()

        if res_hex.startswith(n_num*'00'):
            try:
                print('Found: {} for {} | {}.'.format(res_hex, hex(count), hex_num));
                s.send('ok,{},{}'.format(hex(count),res_hex).encode());
                sys.exit();
                break;
            except socket.error as msg:
                sys.exit();
        if count > 0 and count % 100000 == 0:
            try:
                s.send('Computed {} hashes\n'.format(count).encode());
                print('Computed {} hashes'.format(count))
            except socket.error as msg:
                sys.exit();
        count+=1;
    return "done";

def read_data():
#check for quit signal
    end = False;
    while not end:
        data = s.recv(32).decode();
        if "stop" in data:
            winner_id = data.split(',')[1];
            end = True;
            print('Stop compute. Clientul {} finished first.\n'.format(winner_id));
            print('Quit by pressing Ctrl+C');
            sys.exit();
            break;
    return "stop";

def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work);
        t.daemon = True;
        t.start();

def work():
    while True:
        x = queue.get();
        if x == 1:
            compute();
        if x == 2:
            if read_data() == "stop":
                break;
        queue.task_done();

def create_work():
    for x in JOB_NUM:
        queue.put(x);
    queue.join();

create_threads();
create_work();
