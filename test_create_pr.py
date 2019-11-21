import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from create_pr_replica import Base

class TestCreatePr(TestCase):




    @patch("create_pr_replica.subprocess.getstatusoutput", return_value=Mock())
    def test_run_cmd(self, mock_getstatusoutput):
        baseobj = Base('SREQ1200989')
        cmd = 'dir'
        mock_getstatusoutput.side_effect =[(0, "ABCDEF")]
        baseobj.run_cmd(cmd)
        mock_getstatusoutput.assert_called_with(cmd)

        #mock_getstatusoutput.side_effect =[(1, "ERROR")]
        #cmd = 'ramp'
        #baseobj.run_cmd(cmd)
        #self.assertTrue(mock_getstatusoutput.called, 'Error in executing the command')

    


    @patch('create_pr_replica.os.path')
    @patch('create_pr_replica.os')
    def test_clone_repo(self, mock_os, mock_path):

        cmd = 'rmdir  {}'.format('panorama-ci')

        baseobj = Base('SREQ1200989')
        baseobj.clone_repo()

        # test that path.exists returns false
        mock_path.exists.return_value = False
        self.assertTrue(mock_os.system.called, "Failed to not remove the file if not present.")

        # test that path.esists returns True
        mock_path.exists.return_value = True
        mock_os.system.assert_called_with(cmd)


        #testing the change directory operation
        self.assertTrue(mock_os.chdir.called, 'Failed to change the directory')


    @patch("create_pr_replica.subprocess.getstatusoutput", return_value=Mock())
    def test_get_changed_templates(self, mock_getstatusoutput):
        baseobj = Base('SREQ1200989')
        cmd = 'dir'
        mock_getstatusoutput.side_effect =[(0, "ABCDEF")]
        baseobj.get_changed_templates()
        mock_getstatusoutput.assert_called_with(cmd)

        #mock_getstatusoutput.side_effect =[(1, "ERROR")]
        #cmd = 'ramp'
        #baseobj.get_changed_templates()
        #self.assertTrue(mock_getstatusoutput.called, 'Error in executing the command')

    
    @patch('create_pr_replica.os')
    @patch('create_pr_replica.os.path')
    def test_create_user_playbooks(self, mock_path, mock_os):

        baseobj = Base('SREQ1200989')

        #testing the basename of os.path module

        mock_path.basename.return_value = 'test'
        baseobj.create_user_playbooks()
        self.assertFalse(mock_path.basename.called, 'Failed to call the base function. ')


        #testing the splittext of os.path module
        mock_path.splitext.return_value = 'test again'
        baseobj.create_user_playbooks()
        self.assertFalse(mock_path.splitext.called, 'Failed to call the split text function')

        #testing the getnav of os module

        self.assertFalse(mock_os.getenv.called, 'Failed to call getnav function')


    @patch('create_pr_replica.Base')
    def test_reset_templates(self, MockBase):
        baseobj = MockBase()
        baseobj.reset_templates.return_value = False
        response = baseobj.reset_templates()
        self.assertEqual(response, False)


    @patch('create_pr_replica.Base')
    def test_create_branch(self, MockBase):
        baseobj = MockBase()
        baseobj.create_branch.return_value = False

        response = baseobj.create_branch()

        self.assertEqual(response, False)



    @patch('create_pr_replica.Base')
    def test_setup_hooks(self, MockBase):

        baseobj = MockBase()
        baseobj._setup_hooks.return_value = True
        response = baseobj._setup_hooks()
        self.assertEqual(response, True)


    


    @patch('create_pr_replica.subprocess')
    def test_create_interactive_shell(self, mock_subprocess):

        baseobj = Base('SREQ1200989')

        baseobj.create_interactive_shell()
        self.assertTrue(mock_subprocess.Popen.called, 'Failed to call subprocess.Popen function')
        self.assertFalse(mock_subprocess.Popen.communicate.called, 'Failed to call communication function')





    @patch('create_pr_replica.Base')
    def test_create_commit_message(self, MockBase):

        baseobj = MockBase()
        baseobj.create_commit_message.return_value = True
        response = baseobj.create_commit_message()
        self.assertEqual(response, True)

    

    @patch('create_pr_replica.Base')
    def test_commit_changes(self, MockBase):
        baseobj = MockBase()
        baseobj.commit_changes.return_value = False
        response = baseobj.commit_changes()

        self.assertEqual(response, False)


    @patch('create_pr_replica.Base')
    def test_push_remote(self, MockBase):
        baseobj = MockBase()
        baseobj.push_remote.return_value = False
        response = baseobj.push_remote()
        self.assertEqual(response, False)

    

    


    

    



    @patch('create_pr_replica.os.path')
    @patch('create_pr_replica.os')
    def test_rm(self, mock_os, mock_path):

        baseobj = Base('SREQ1200989')
        # set up the mock
        mock_path.isfile.return_value = False
        file_name= 'c:/atdas/home/file.txt'
        baseobj.rm(file_name)
        # test that the remove call was NOT called.
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")
        # make the file 'exist'
        mock_path.isfile.return_value = True
        baseobj.rm(file_name)
        mock_os.remove.assert_called_with(file_name)
    
        



    

        




if __name__ == '__main__':
    unittest.main()

