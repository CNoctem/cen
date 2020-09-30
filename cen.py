import os
import sys

import git
import config
from git import RemoteProgress

import pomparse
import util

import cache

ps = os.path.sep


class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)


def init():
    cache.cen_root_dir = util.get_cen_root()
    cache.dotcen_path = cache.cen_root_dir + ps + '.cen'
    cache.args.inject('clone', clone_all, n_params=1)
    cache.args.inject('versions', get_all_versions)
    cache.args.inject('version', get_version)
    cache.args.inject('whereami', print_location)
    cache.args.inject('info', print_info)

    cache.scm_path = util.read_dotcen('scm')
    cache.config_path = util.read_dotcen('config')
    cache.infra_path = util.read_dotcen('infra')

    return cache


def print_info():
    print('cen project root:', cache.cen_root_dir, '\n')
    print('             scm:', cache.scm_path)
    print('          config:', cache.config_path)
    print('           infra:', cache.infra_path, '\n')
    print('    currently in:', util.where_am_i(), '\n')

def print_location():
    print(util.where_am_i())


def get_version():
    pass


def get_all_versions():
    get_scm_version()
    get_config_version()


def get_scm_version():
    scm_pom = cache.scm_path + ps + 'pom.xml'
    print('[scm   ] ' + util.last_path_elem(cache.scm_path) + ':' + pomparse.get_version(scm_pom))


def get_config_version():
    with open(cache.config_path + ps + 'appconf' + ps + 'dc.ini') as confdcini:
        for l in confdcini.readlines():
            if l.lstrip().startswith(config.PROPERTIES['conf.dcini.version.prefix']):
                print('[config] ' + util.last_path_elem(cache.config_path) + l[l.index(':'):])


def clone_all(module_name_arr):
    module_name = module_name_arr[0]
    short_module_name = util.short_mod_name(module_name)
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

    util.write_to_dotcen('scm', scm_dest_path)
    util.write_to_dotcen('config', config_dest_path)
    util.write_to_dotcen('infra', infra_dest_path)


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
    cache = init()
    cache.args.parse(sys.argv[1:])
