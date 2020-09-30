import os

PROPFILE_DELIM = '='

CONFIG_REPO_BASE_URL = 'https://{username}:{password}@config.cicd.erste.hu/'
SCM_REPO_BASE_URL = 'https://{username}:{password}@scm.cicd.erste.hu/'

PROPERTIES = {'config.dir.name': 'config', 'config.branch.name': 'erste_d10', 'scm.branch.name': 'developer',
              'conf.dcini.version.prefix': 'export DC_ARTIFACT_FULLNAME='}


def get_auth_config_repo_base(usr, pwd):
    return CONFIG_REPO_BASE_URL.replace('{username}', usr).replace('{password}', pwd)


def get_auth_scm_repo_base(usr, pwd):
    return SCM_REPO_BASE_URL.replace('{username}', usr).replace('{password}', pwd)


def short_mod_name(module_name):
    if '/' not in module_name:
        return module_name
    return module_name[module_name.index('/') + 1:]

def last_path_elem(path):
    return os.path.basename(os.path.normpath(path))

def read_dotcen(key):
    with open(os.getcwd() + os.path.sep + '.cen', 'r') as cenfile:
        for l in cenfile.readlines():
            if PROPFILE_DELIM in l:
                k, v = l.split(PROPFILE_DELIM)
                if key == k:
                    return v.strip()
        return None


def write_to_dotcen(key, val):
    path = os.getcwd() + os.path.sep + '.cen'
    lines = [key + PROPFILE_DELIM + val]
    mode = 'a' if os.path.exists(path) else 'w'
    if mode == 'a':
        with open(path, 'r') as cenfile:
            for l in cenfile.readlines():
                l = l.strip()
                if len(l) == 0:
                    continue
                if l[0] == '#':
                    lines.append(l)
                elif PROPFILE_DELIM in l:
                    k, v = l.split(PROPFILE_DELIM)
                    if k != key:
                        lines.append(l)
    with open(path, mode) as cenfile:
        for l in lines:
            cenfile.write(l + '\n')
