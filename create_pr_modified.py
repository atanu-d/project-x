#!/usr/bin/python
"""Script to create github PR for creating ansible playbook change"""
import commands
import logging
import os
import re
import sys
import subprocess

REPO = \
    'git@panwgithub.paloaltonetworks.local:Infra-Network/panorama-ci.git'
PIPE = subprocess.PIPE


class Base(object):
    '''
    This is a class for creating a PR.
    Attributes:
        sn_req(string): Service now request ID.
    '''

    def __init__(self, sn_req):
        '''Constructor for base class.
        Args:
            sn_req(string): Service now request ID.
        '''

        self.sn_req = sn_req
        self.local_repo_path = os.path.join(os.getcwd(), sn_req + '/panorama-ci')
        self.sreq = sn_req
        self.commit_message = None
        self.changed_playbook_templates = []
        log_file = '/tmp/'+os.path.splitext(os.path.basename(__file__))[0]+'.log'
        logging.basicConfig(filename=log_file, filemode='a+', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.warning('This will get logged to a file')

    @staticmethod
    def run_cmd(cmd):
        '''function to run command in linux shell environment.
        Args:
            cmd(string): command as string with argument.
        Returns:
            exit with status 1 if command fails.
        '''

        code, output = commands.getstatusoutput(cmd)

        logging.info('command = %s', ' '.join(cmd))
        logging.info('command output = %s', output)
        logging.info(output)
        if code != 0 :
            print 'command failed to get changed files'
            sys.exit(1)


    def clone_repo(self):
        '''
        Function to clone repo.
        Removes old git repo if exists and creates new one.
        '''

        if os.path.exists(self.local_repo_path):
            os.system('rm -rf %s' % self.local_repo_path)
        cmd = 'mkdir -p %s' % self.local_repo_path
        self.run_cmd(cmd)
        cmd = 'git clone %s %s' % (REPO, self.local_repo_path)
        self.run_cmd(cmd)
        os.chdir(self.local_repo_path)


    def get_changed_templates(self):
        '''function to get changed templates.'''

        code, output = commands.getstatusoutput('git diff HEAD --name-only')
        if code != 0:
            print 'command failed to get changed files'
            sys.exit(1)
        files = output.split('\n')
        if files:
            self.changed_playbook_templates = files
        print(files)


    def create_user_playbooks(self):
        '''function to copy changed playbook files to user_playbook dir.'''

        for f in self.changed_playbook_templates:
            base = os.path.basename(f)
            f_name = os.path.splitext(base)[0]
            extension = os.path.splitext(base)[1]
            cmd = ('cp %s user_playbooks/%s_%s_%s%s'  % 
                    (f, f_name, self.sn_req, os.getenv('USER'), extension))
            self.run_cmd(cmd)


    def reset_templates(self):
        '''function to unstage and reset template files.'''

        for f in self.changed_playbook_templates:
            cmd = 'git reset HEAD %s' % f
            self.run_cmd(cmd)
            cmd = 'git checkout -- %s' % f
            self.run_cmd(cmd)


    def create_branch(self):
        '''function to create branch.'''

        cmd = 'git branch %s' % self.sreq
        self.run_cmd(cmd)
        cmd = 'git push origin %s' % self.sreq
        self.run_cmd(cmd)
        cmd = 'git checkout %s' % self.sreq
        self.run_cmd(cmd)
        self._setup_hooks()

        return True


    def _setup_hooks(self):
        '''setup precommit hooks and commit message templates.'''

        cmd = 'git config --local commit.template .gitmessage'
        self.run_cmd(cmd)
        cmd = 'ln -s ../../hooks/commit-msg .git/hooks/commit-msg'
        self.run_cmd(cmd)

        return True


    def create_interactive_shell(self):
        '''function to create interactive shell for users to edit ansible playbook.'''

        os.chdir(self.local_repo_path)
        print 'Please use the shell to make changes in the ansible playbook'
        print 'Once done with making changes, save file and press CTL+d to exit'
        proc = subprocess.Popen(['/bin/bash'])
        proc.communicate()


    def create_commit_message(self):
        ''''function to create commit message.'''

        summary = raw_input('Please add summary sentense to describe what changes'
                            ' you are making. Please make sure summary is less than'
                            ' 50 characters long: ')
        business_reason = raw_input('Please explain in couple of lines'
                                    ' what is the business purpose and impact'
                                    ' of this change: ')
        change_type = raw_input('Is this Normal change or Expedite Change?'
                                ' (Just type Normal/Expedite): ')
        u_category = raw_input('Please provide u_catagoty (Enhancement/Bug): ')
        start_date = raw_input('Please provide start date in YYYY-MM-DD HH:MM format: ')
        end_date = raw_input('Please provide end date in YYYY-MM-DD HH:MM format: ')
        commit_message = ('{}\n\n'
                          '{}\n'
                          '{} change\n\n'
                          'u_category: {}\n'
                          'servicenow_ID: {}\n'
                          'assignment_group: Network-Security-HCL\n'
                          'start_date: {} PDT\n'
                          'end_date: {} PDT')
        self.commit_message = commit_message.format(summary,
                                                    business_reason,
                                                    change_type,
                                                    u_category,
                                                    self.sreq,
                                                    start_date,
                                                    end_date)
        
        return True


    def commit_changes(self):
        '''function to commit changes.'''

        cmd = 'git add *'
        self.run_cmd(cmd)
        cmd = 'git commit -m'
        cmd = cmd + self.commit_message
        self.run_cmd(cmd)

        return True


    def push_remote(self):
        '''function to push changes to remote branch.'''

        cmd = 'git push --set-upstream origin %s' % self.sreq
        self.run_cmd(cmd)

        return True


def main():
    '''main function.'''

    tmp = raw_input('Please enter Service-Now INC or SREQ number: ')
    sreq = tmp.strip()
    if len(sreq) < 10:
        print 'INC/SREQ number is not valid'
        sys.exit(1)
    if not re.match(r'SREQ|INC', sreq):
        print 'Service Now ID is not valid'
    git = Base(sreq)
    print 'Creating branch %s' % sreq
    print 'Cloning Repo'
    git.clone_repo()
    print 'creating branch %s' % sreq
    git.create_branch()
    print '----------- Starting Interactive Shell, Press CTL+d to exit -----------'
    git.create_interactive_shell()
    git.get_changed_templates()
    git.create_user_playbooks()
    git.reset_templates()
    git.create_commit_message()
    git.commit_changes()
    print '----------- Pushing changes to remote branch -------------'
    git.push_remote()
    print '----------- Please go to github and create pull request ----------'


if __name__ == '__main__':
    main()