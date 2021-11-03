# Distributed_computation
Distributed computation app where clients connect to a server who distributes a computation problem. The first client that finds the solution wins.

Requirement
Two programs will be created in Python 3.x - a client that will run in multiple instances and a single server -
to allow the distributed solution of a computationally intensive problem, similar to
Bitcoin mining (but simplified).

Description
The server will listen on at least one port, namely port = (team number + 12) * 100 (to be> 1024). Can
use additional ports as desired.
Teams with even numbers will use the TCP protocol and the other UDPs - see the corresponding functions in the lab
of sockets. Those using UDP do not need to implement additional retransmission methods (for
not to complicate their task compared to those with TCP).
The server program will have as parameters in the command line an n number and a string
(text representation of a hexadecimal number of the type A7C02215FC). Alternatively, if called without
parameters, it will require the introduction of n and string.
The goal will be for the client to find a hexadecimal value called seed which, concatenated at the beginning
of the string expressed in hexadecimal, to result in an MD5 hash of the hexadecimal number
concatenated seed | string beginning with n bytes of value 00. Symbol | is the concatenation operation,
for example 1234 | ABCD = 1234ABCD
For example, for n = 3, an acceptable MD5 hash will be:
0x00000051893FD5680A631B2419C1445E05


How to launch the application:
1. Launch server.py. with the two parameters (n and the hex string) Ex: ./server.py 3 abcdf
2. Each client with its parameter (server IP address) is launched. Ex: ./client.py 127.0.0.1

####
Server.py implementation
###
A thread-based approach is used to be able to accept multiple connections while the server is receiving
displays data from customers or sends data to customers, so there are 3 threads.
All connections and addresses are stored in lists.
The server is launched together with the two parameters (n and hex string).
Once launched, the server waits for at least 2 clients to connect.
Once connected, the server sends the problem data to them and the calculation process is
launched.
The server expects regular data from clients. If the message contains the string "ok", then
it means that customer has found the solution. If not, the server displays the message received from the client.
If the solution was found, the severity displays who found the solution first, send the id to that one
client to all clients and close all connections.

###
Client.py implementation
###
Also a thread-based approach to allow computation at the same time as
reading messages received from the server and sending messages to the server.
The client is launched together with the IP address parameter of the server.
The client starts with an initial reading of the data sent by the server where it is waiting for three pieces of information
client_id, n_num, hex_num. Based on this information, the client displays the id assigned to it and
problem data.
The client uses an infinite loop in which an incremented counter in each iteration is
transformed into hex and concatenated to the hex string given initially. The hash is generated and checked
if it starts with n_num * '00'. (where n_num is n given initially).
Once the solution is found, the string '' ok ', seed, hash' is sent to the server and the execution stops
In parallel, if the solution has not been found yet, the client reads entries from the server. If
read the 'stop' string when another client has already terminated. The customer will parse the customer id
which failed (client_id sent by the server together with the message 'stop').

###
Messages used
###
The application uses only two protocol messages: 'ok' and 'stop'.
The 'ok' message is sent by the client to the server when the client has found the solution.
based on the message, the server launches the winner 's communication logic and commands
cessation of calculations.

The 'stop' message is sent by the server to the client upon receipt of the 'ok' message. Has the role
to signal to all customers (can be optimized by sending only customers who
they did not win) the fact that they can stop the calculations.
