import requests
import time
import os


'''
this is just for git checking purpose

'''

#new changes for the test..

class Blog:
    def __init__(self, name):
        self.name = name

    def posts(self):
        response = requests.get("https://jsonplaceholder.typicode.com/posts")

        return response.json()


    def __repr__(self):
        return '<Blog: {}>'.format(self.name)

    def sum(self, a, b):

        return a+b


    def work_on(self):
        path = os.getcwd()
        print(f'Working on {path}')
        return path
		

	
		


def main():
    obj = Blog('Atanu')
    #print(obj.__repr__())
    #print(obj.sum(3,4))
    #print(obj.posts())
    obj.work_on()

if __name__ == '__main__':
	main()