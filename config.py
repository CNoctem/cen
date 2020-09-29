REPO_BASE_URL = 'https://{username}:{password}@config.cicd.erste.hu/'

def get_auth_repo_base(usr, pwd):
    return REPO_BASE_URL.replace('{username}', usr).replace('{password}', pwd)