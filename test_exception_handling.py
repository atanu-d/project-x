import unittest
from unittest import mock
from exception_handling import ExceptionHandling

class TestExceptionHandling(unittest.TestCase):
    
    @mock.patch("exception_handling.Exception")
    def test_handling_exception(self, mock_exception):
        print("\ntest_handling_exception".upper())
        e = ExceptionHandling()
        e.handling_exception(2,1)        
        mock_exception.assert_not_called()

        mock_exception.side_effect = ZeroDivisionError
        self.assertIsNone(e.handling_exception(2,0))

        mock_exception.side_effect = TypeError
        self.assertIsNone(e.handling_exception(2,'abc'))


    @mock.patch("exception_handling.Exception")
    def test_exception_handling_method2(self, mock_exception):
        print("\ntest_exception_handling_method2".upper())
        e = ExceptionHandling()
        e.without_handling_exception(2,1)        
        mock_exception.assert_not_called()
        
        with self.assertRaises(ZeroDivisionError):
            print( "ZeroDivisionError")
            e.without_handling_exception(2,0)

        with self.assertRaises(TypeError):
            print( "TypeError")
            e.without_handling_exception(2,'abc')  


   
if __name__ == "__main__":
    unittest.main()

