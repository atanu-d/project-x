import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from main import Blog



class TestMain(TestCase):
    @patch('main.Blog')

    def test_blog_posts(self, MockBlog):
        blog = MockBlog()

        blog.posts.return_value = [
			{
				'userId': 1,
				'id': 1,
				'title': 'Test Title',
				'body': 'Far out in the uncharted backwaters of the unfashionable  end  of the  western  spiral  arm  of  the Galaxy\ lies a small unregarded yellow sun.'
				}
		]

        response = blog.posts()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0],dict)
        blog.posts.assert_called_with()


    @patch('main.Blog.sum')

    def test_sum(self, sum):
        sum.return_value = 9
        self.assertEqual(sum(2,3), 9)
        #self.assertEqual()
        #blog.sum.assert_called_with(1,2)


    @patch('main.os')

    def test_using_decorator(self, mock_os):
        Blog.work_on(self)
        mock_os.getcwd.assert_called_once()
        



if __name__ == '__main__':
    unittest.main()