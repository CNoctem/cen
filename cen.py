import getpass
import os
import sys

import git
import config
from git import RemoteProgress

from argparse import Args


class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def init():
    args = Args()
    args.inject('clone', clone_all, n_params=1)
    return args

def clone_all(module_name):
    print('Cloning MODULE ', module_name, 'to', os.getcwd())
    dest_path = os.getcwd()
    usr, pwd = authenticate()
    repo_base = config.get_auth_repo_base(usr, pwd)
    clone_repo(repo_base + module_name + '.git', dest_path + '\\' + module_name)
    clone_repo(repo_base + module_name + '-infra.git', dest_path + '\\' + module_name + '-infra')

def clone_repo(repo_url, dest_path):
    print('Cloning into %s' % dest_path)
    git.Repo.clone_from(repo_url, dest_path,
                        branch='erste_d10', progress=CloneProgress())


def authenticate():
    username = input('username: ')
    password = getpass.getpass('password: ')
    return username, password


if __name__ == '__main__':
    args = init()
    args.parse(sys.argv[1:])

