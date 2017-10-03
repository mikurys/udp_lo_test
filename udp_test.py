#!/usr/bin/env python3
import socket
import sys
import time
import argparse
import threading


def run_server(port, thread_num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port + thread_num))
    start_time = time.time()
    packet_counter = 0
    size_counter = 0
    while True:
        data = sock.recv(65535)
        packet_counter += 1
        size_counter += len(data)
        message = data.decode()
        assert message[0] == 'a', 'bad message'
        assert message[-1] == 'z', 'bad message'
        if packet_counter % 100000 == 0:
            print('thread:', thread_num, 'speed:', ((size_counter*8)/(1000*1000*1000)) / (time.time() - start_time), 'Gbits/s')


def run_client(port, packet_size, thread_num):
    assert packet_size >= 2, 'bad message size'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = ('a' + 'x' * (packet_size - 2) + 'z').encode()
    while True:
        sock.sendto(data, ('127.0.0.1', port + thread_num))

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='UDP client/server to test localhost speed.\n Usage: first run in client mode, next run in server mode')
    arg_parser.add_argument('-c', '--client', action='store_true', help='run in client mode')
    arg_parser.add_argument('-s', '--server', action='store_true', help='run in server mode')
    arg_parser.add_argument('--size', type=int, default=1000, help='packet size in bytes; work in client mode (in server mode ignored)')
    arg_parser.add_argument('-t', '--threads', type=int, default=1, help='number of threads')
    arg_parser.add_argument('-p', '--port', type=int, default=9999, help='port number')
    args = arg_parser.parse_args()

    threads = []
    for i in range(args.threads):
        if args.server:
            threads.append(threading.Thread(target=run_server, args=(args.port, i)))
        elif args.client:
            threads.append(threading.Thread(target=run_client, args=(args.port, args.size, i)))
        threads[i].start()

    for i in range(args.threads):
        threads[i].join()
