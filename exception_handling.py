#!/usr/bin/python

class ExceptionHandling():
    '''
    This class is for handling exceptions
    '''

    def handling_exception(self, num1, num2):
        '''
            Once exception is handled, it is swallowed and not returned to test function
            calling it.
        '''
        print("exception_handling called....{0} {1}".format(num1, num2))
        try:
            division = num1/num2
            print("{0} divided by {1} is {2}".format(num1, num2, division))
        except ArithmeticError as e:
            print("Cannot divide {0} by {1}, {2}".format(num1, num2, e))
        except TypeError as e:
            print('Error, ', e)


    def without_handling_exception(self, num1, num2):
        '''
            Without handling the exception we should raise the exception
            to be tested in unittesting cases
        '''
        division = num1/num2
        print("{0} divided by {1} is {2}".format(num1, num2, division))


if __name__== "__main__":
    eh_obj = ExceptionHandling()
    
    eh_obj.handling_exception(2,1)
    eh_obj.handling_exception(2,0)
    eh_obj.handling_exception(2,'abc')

    #eh_obj.without_handling_exception(2,1)
    #eh_obj.without_handling_exception(2,0)
    #eh_obj.without_handling_exception(2, 'abc')
    
