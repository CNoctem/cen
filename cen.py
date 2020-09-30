import getpass
import os
import sys

import git
import config
from git import RemoteProgress

from argparse import Args

ps = os.path.sep

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def init():
    args = Args()
    args.inject('clone', clone_all, n_params=1)
    return args

def clone_all(module_name_arr):
    module_name = module_name_arr[0]
    short_module_name = config.short_mod_name(module_name)
    config_dir_name = config.PROPERTIES['config.dir.name']
    print('Cloning MODULE ', short_module_name, 'to', os.getcwd())
    dest_path = os.getcwd()
    usr, pwd = authenticate()

    config_repo_base = config.get_auth_config_repo_base(usr, pwd)
    clone_repo(config_repo_base + module_name + '.git', dest_path + ps + config_dir_name + ps + short_module_name, config.PROPERTIES['config.branch.name'])
    clone_repo(config_repo_base + module_name + '-infra.git', dest_path + ps + config_dir_name + ps + short_module_name + '-infra', config.PROPERTIES['config.branch.name'])

    scm_repo_base = config.get_auth_scm_repo_base(usr, pwd)
    clone_repo(scm_repo_base + module_name + '.git', dest_path + ps + short_module_name, config.PROPERTIES['scm.branch.name'])


def clone_repo(repo_url, dest_path, branch):
    print('Cloning into %s' % dest_path)
    git.Repo.clone_from(repo_url, dest_path,
                        branch=branch, progress=CloneProgress())


def authenticate():
    # username = input('username: ')
    # password = getpass.getpass('password: ')
    # return username, password

    return 'smaso_kovacsg', 'P4mic8cE'


if __name__ == '__main__':
    args = init()
    args.parse(sys.argv[1:])

