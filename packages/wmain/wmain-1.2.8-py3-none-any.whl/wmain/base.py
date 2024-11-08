import os

def create_dir(dir_path):
    os.makedirs(dir_path, exist_ok=True)
    
def create_path(file_path):
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
def execute_cmd(cmd: str):
    r = os.popen(cmd)
    output = r.read()
    r.close()
    return output

def execute_powershell(cmd: str):
   return execute_cmd(f'powershell -Command "{cmd}"')