#!/usr/bin/python
import unittest
from unittest import mock
import socket
from socket_programming import SocketProgram
import warnings


class TestSocketProgram(unittest.TestCase):
    s = SocketProgram()

    @mock.patch("socket_programming.Exception")
    def test_create_socket(self, mock_exception):
        print("\nTEST THE SOCKET CREATION FUNCTION\n")
        
        self.s.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertTrue(mock_exception.assert_not_called(), 'Exception called')

        with self.assertRaises(TypeError):
            print("\nTypeError raised")
            mock_exception.side_effect = TypeError            
            self.s.create_socket('abc', 'def')

    @mock.patch("socket_programming.Exception")
    def test_get_host_ip(self, mock_exception):
        print("\nTEST THE GETTING HOST IP BY NAME FUNCTION\n")
        self.s.get_host_ip("www.google.com")
        mock_exception.assert_not_called()

        with self.assertRaises(socket.gaierror):
            mock_exception.side_effect = socket.gaierror            
            self.s.get_host_ip("www.google_vani.com")

    @mock.patch("socket_programming.Exception")
    def test_create_connection(self, mock_exception):
        print("\nTEST THE CREATE CONNECTION FUNCTION\n")
        self.s.create_connection(1000)
        mock_exception.assert_not_called()

        with self.assertRaises(TypeError):
            mock_exception.side_effect = TypeError            
            self.s.create_connection('aaaa')


if __name__ == "__main__":
    unittest.main()
    
        
