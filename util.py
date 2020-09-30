import os
from pathlib import Path

import cache
import config

PROPFILE_DELIM = '='


def short_mod_name(module_name):
    if '/' not in module_name:
        return module_name
    return module_name[module_name.index('/') + 1:]


def last_path_elem(path):
    return os.path.basename(os.path.normpath(path))


def get_cen_root():
    cenroot = os.getcwd()
    while not '.cen' in os.listdir(cenroot):
        cenroot = os.path.abspath(os.path.join(cenroot, os.pardir))
    return cenroot


def read_dotcen(key):
    with open(cache.dotcen_path, 'r') as cenfile:
        for l in cenfile.readlines():
            if PROPFILE_DELIM in l:
                k, v = l.split(PROPFILE_DELIM)
                if key == k:
                    return v.strip()
        return None


def write_to_dotcen(key, val):
    lines = [key + PROPFILE_DELIM + val]
    mode = 'a' if os.path.exists(cache.dotcen_path) else 'w'
    if mode == 'a':
        with open(cache.dotcen_path, 'r') as cenfile:
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
    with open(cache.dotcen_path, mode) as cenfile:
        for l in lines:
            cenfile.write(l + '\n')


def where_am_i():
    if cache.scm_path in os.getcwd():
        return 'scm'
    elif cache.config_path in os.getcwd():
        return 'config'
    elif cache.infra_path in os.getcwd():
        return 'infra'
    elif cache.cen_root_dir == os.getcwd():
        return 'cen root'
    elif cache.cen_root_dir + os.path.sep + config.PROPERTIES['config.dir.name'] == os.getcwd():
        return 'config root'
    else:
        return 'I have no idea where you might be.'
