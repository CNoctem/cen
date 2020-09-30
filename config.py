CONFIG_REPO_BASE_URL = 'https://{username}:{password}@config.cicd.erste.hu/'
SCM_REPO_BASE_URL = 'https://{username}:{password}@scm.cicd.erste.hu/'

PROPERTIES = {'config.dir.name': 'config', 'config.branch.name': 'erste_d10', 'scm.branch.name': 'developer'}

def get_auth_config_repo_base(usr, pwd):
    return CONFIG_REPO_BASE_URL.replace('{username}', usr).replace('{password}', pwd)

def get_auth_scm_repo_base(usr, pwd):
    return SCM_REPO_BASE_URL.replace('{username}', usr).replace('{password}', pwd)

def short_mod_name(module_name):
    if '/' not in module_name:
        return module_name
    return module_name[module_name.index('/') + 1:]
