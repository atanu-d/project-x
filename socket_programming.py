#!/usr/bin/python
import socket
import sys


class SocketProgram():

    def create_socket(self, net, stream, call= None):
        print(net, stream, call)
        try:
            self.sock = socket.socket(net, stream)
            print("Socket created successfully")
            if call == None:
                self.sock.close()
        except Exception as err:
            print("Socket creation failed with error {}".format(err))
            raise
        
        

    def get_host_ip(self, url):
        self.url = url
        try:
            self.host_ip = socket.gethostbyname(url)
            print("HOST IP: {}".format(self.host_ip))
        except socket.gaierror as e:
            print("Error getting host IP")
            #sys.exit(1)
            raise

    def create_connection(self, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM, "connection")
        self.get_host_ip("www.google.com")
        self.sock.connect((self.host_ip, port))
        print("The socket succesfully connected to {0} on port {1}".format(self.url.split('.')[1], port))
        self.sock.close()


if __name__=="__main__":
    s = SocketProgram()
    #s.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.create_socket("AF_INET", socket.SOCK_STREAM)
    #s.get_host_ip("www.google.com")
    s.create_connection(9000)
