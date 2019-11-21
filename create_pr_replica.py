import logging
import os
import re
import sys
import subprocess


REPO = \
    'git@panwgithub.paloaltonetworks.local:Infra-Network/panorama-ci.git'
PIPE = subprocess.PIPE


class Base(object):

    def __init__(self, sn_req):
        self.sn_req = sn_req
        self.local_repo_path = os.path.join(os.getcwd() + '/panorama-ci')
        self.sreq = sn_req
        self.commit_message = None
        self.changed_playbook_templates = []
        #log_file = '/tmp/'+os.path.splitext(os.path.basename(__file__))[0]+'.log'
        #logging.basicConfig(filename=log_file, filemode='a+', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        #logging.warning('This will get logged to a file')
        #cmd = 'mkdir {}'.format('panorama-ci')
        #os.system(cmd)
        #print(cmd)

    def run_cmd(self, cmd):
        '''function to run command in linux shell environment.

        Args:
            cmd(list): command as list with argument.

        Returns:
            exit with status 1 if command fails.
        '''

        code, output = subprocess.getstatusoutput(cmd)
        print("Exit Code: {0} \n Output Data: {1}".format(code, output))
        if code != 0:
            print("Error Executing the command")
            exit(1)
        else:
            print(output)



    def clone_repo(self):

        print(os.path.exists(self.local_repo_path))

        if os.path.exists(self.local_repo_path):
            print('Dir exists')
            cmd = 'rmdir  {}'.format('panorama-ci')
            os.system(cmd)
        else:
            print('Path does not exist')

        if os.path.exists(self.local_repo_path):
            print('Dir exists')
        else:
            print('Dir does not exist')

        os.chdir(self.local_repo_path)


    def _setup_hooks(self):
        '''setup precommit hooks and commit message templates.'''

        cmd = 'git config --local commit.template .gitmessage'
        self.run_cmd(cmd)
        cmd = 'ln -s ../../hooks/commit-msg .git/hooks/commit-msg'
        #self.run_cmd(cmd)

        return True

    
    def create_branch(self):
        '''function to create branch.'''

        cmd = 'git branch %s' % self.sreq
        #self.run_cmd(cmd)
        cmd = 'git push origin %s' % self.sreq
        #self.run_cmd(cmd)
        cmd = 'git checkout %s' % self.sreq
        #self.run_cmd(cmd)
        #self._setup_hooks()

        return True

    def create_interactive_shell(self):
        '''function to create interactive shell for users to edit ansible playbook.'''

        #os.chdir(self.local_repo_path)
        print ('Please use the shell to make changes in the ansible playbook')
        print ('Once done with making changes, save file and press CTL+d to exit')
        proc = subprocess.Popen(["mkdir", "hello_world"], stdout=subprocess.PIPE)
        print('process: ', proc)
        proc.communicate()


    def commit_changes(self):
        '''function to commit changes.'''

        cmd = 'git add *'
        #self.run_cmd(cmd)
        cmd = 'git commit -m'
        #cmd.append(self.commit_message)
        #self.run_cmd(cmd)

        return True


    def push_remote(self):
        '''function to push changes to remote branch.'''

        cmd = 'git push --set-upstream origin %s' % self.sreq
        #self.run_cmd(cmd)

        return True

    def create_commit_message(self):

        return True

    def get_changed_templates(self):

        code, output = subprocess.getstatusoutput('dir')

        if code != 0:
            print("Error Executing the command")
            exit(1)
        
        files = output.split('\n')
        if files:
            self.changed_playbook_templates = files
        #print(files)

    def create_user_playbooks(self):
        '''function to copy changed playbook files to user_playbook dir.'''

        for f in self.changed_playbook_templates:
            base = os.path.basename(f)
            #print(base)
            f_name = os.path.splitext(base)[0]
            print(f_name)
            extension = os.path.splitext(base)[1]
            print(extension)
            cmd = ('cp %s user_playbooks/%s_%s_%s%s'  % 
                    (f, f_name, self.sn_req, os.getenv('USER'), extension))
            #self.run_cmd(cmd)

    
    def reset_templates(self):
        '''function to unstage and reset template files.'''

        for f in self.changed_playbook_templates:
            cmd = 'git reset HEAD %s' % f
            #self.run_cmd(cmd)
            cmd = 'git checkout -- %s' % f
            #self.run_cmd(cmd)

        return True

    def rm(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)
        




def main():
    sreq = 'SREQ1200989'
    sreq = sreq.strip()
    git = Base(sreq)
    #git.clone_repo()

    #git.run_cmd('ramp')
    #git.create_interactive_shell()
    git.get_changed_templates()
    git.create_user_playbooks()



if __name__ == '__main__':
    main()
