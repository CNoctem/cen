import os
import sys

import git
from git import RemoteProgress

import cache
import config
import pomparse
import util

ps = os.path.sep


class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)


def print_info():
    print('cen project root:', cache.cen_root_dir, '\n')
    print('             scm:', cache.scm_path)
    print('          config:', cache.config_path)
    print('           infra:', cache.infra_path, '\n')
    print('    currently in:', util.where_am_i(), '\n')


def print_location():
    print(util.where_am_i())


def get_version():
    w = util.where_am_i()
    if w in ['config root', 'config']:
        print_config_version()
    elif w in ['scm', 'cen root']:
        print_scm_version()
        if w == 'cen root':
            print_config_version()
    elif w == 'infra':
        print('Infra version is unimportant.')


def set_version(newversion):
    w = util.where_am_i()
    if w == 'scm':
        print('[scm   ] ' + util.last_path_elem(cache.scm_path) + ':' + get_scm_version(), '->', newversion)
    elif w in ['config', 'config root']:
        print('[config] ' + get_config_version(), '->', newversion)
        if util.yes_no_quit():
            util.change_config_version(newversion)
    elif w == 'cen root':
        print('[scm   ] ' + util.last_path_elem(cache.scm_path) + ':' + get_scm_version(), '->', newversion)
        print('[config] ' + get_config_version(), '->', newversion)
    else:
        print('Navigate to scm or config to their versions individually.', 'cd ' + cache.scm_path)
        print('Navigate to cen root to set both versions.', 'cd ' + cache.cen_root_dir)


def get_all_versions():
    print_scm_version()
    print_config_version()


def print_scm_version():
    print('[scm   ] ' + util.last_path_elem(cache.scm_path) + ':' + get_scm_version())


def get_scm_version():
    scm_pom = cache.scm_path + ps + 'pom.xml'
    return pomparse.get_version(scm_pom)


def print_config_version():
    print('[config] ' + get_config_version())


def get_config_version():
    with open(cache.config_path + ps + 'appconf' + ps + 'dc.ini') as confdcini:
        for l in confdcini.readlines():
            if l.lstrip().startswith(config.PROPERTIES['conf.dcini.version.prefix']):
                return util.last_path_elem(cache.config_path) + l[l.index(':'):]


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
