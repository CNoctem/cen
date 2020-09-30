import getpass
import os
import sys

import git
import config
from git import RemoteProgress

import pomparse
from argparse import Args

ps = os.path.sep


class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)


def init():
    args = Args()
    args.inject('clone', clone_all, n_params=1)
    args.inject('versions', get_all_versions)
    return args


def get_all_versions():
    scm_path = config.read_dotcen('scm')
    config_path = config.read_dotcen('config')
    infra_path = config.read_dotcen('infra')

    scm_pom = scm_path + ps + 'pom.xml'
    print('[scm   ] ' + config.last_path_elem(scm_path) + ':' + pomparse.get_version(scm_pom))

    with open(config_path + ps + 'appconf' + ps + 'dc.ini') as confdcini:
        for l in confdcini.readlines():
            if l.lstrip().startswith(config.PROPERTIES['conf.dcini.version.prefix']):
                print('[config] ' + config.last_path_elem(config_path) + l[l.index(':'):])


def clone_all(module_name_arr):
    module_name = module_name_arr[0]
    short_module_name = config.short_mod_name(module_name)
    config_dir_name = config.PROPERTIES['config.dir.name']
    print('Cloning MODULE ', short_module_name, 'to', os.getcwd())
    dest_path = os.getcwd()
    usr, pwd = authenticate()

    config_repo_base = config.get_auth_config_repo_base(usr, pwd)

    config_dest_path = dest_path + ps + config_dir_name + ps + short_module_name
    clone_repo(config_repo_base + module_name + '.git', config_dest_path, config.PROPERTIES['config.branch.name'])

    infra_dest_path = dest_path + ps + config_dir_name + ps + short_module_name + '-infra'
    clone_repo(config_repo_base + module_name + '-infra.git', infra_dest_path, config.PROPERTIES['config.branch.name'])

    scm_repo_base = config.get_auth_scm_repo_base(usr, pwd)

    scm_dest_path = dest_path + ps + short_module_name
    clone_repo(scm_repo_base + module_name + '.git', scm_dest_path, config.PROPERTIES['scm.branch.name'])

    config.write_to_dotcen('scm', scm_dest_path)
    config.write_to_dotcen('config', config_dest_path)
    config.write_to_dotcen('infra', infra_dest_path)


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
