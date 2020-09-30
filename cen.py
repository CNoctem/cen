import os
import sys

import cache
import commands
import util

ps = os.path.sep


def init():
    cache.cen_root_dir = util.get_cen_root()
    cache.dotcen_path = cache.cen_root_dir + ps + '.cen'
    cache.args.inject('clone', commands.clone_all, n_params=1)
    cache.args.inject('versions', commands.get_all_versions)
    cache.args.inject('version', commands.get_version)
    cache.args.inject('whereami', commands.print_location)
    cache.args.inject('info', commands.print_info)
    cache.args.inject('setversion', commands.set_version, n_params=1)

    cache.scm_path = util.read_dotcen('scm')
    cache.config_path = util.read_dotcen('config')
    cache.infra_path = util.read_dotcen('infra')

    return cache

if __name__ == '__main__':
    cache = init()
    cache.args.parse(sys.argv[1:])
