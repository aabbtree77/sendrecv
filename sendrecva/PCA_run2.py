import subprocess
import json
import time
import sys
import datetime

# This code is part of an experiment where two computers
# communicate via github. It is to be executed on the computer A:
# inside a properly git cloned and token-setup git repo "sendrecva".

# One must have two github repos on the github server and their clones on the resp. machines
# with GITHUB_ACCESS_TOKEN set inside resp. bash files as indicated in http://www.compciv.org/recipes/devops/git-and-github-setup/
# git remote rm origin
# git remote add origin https://aabbtree77:$GITHUB_ACCESS_TOKEN@github.com/aabbtree77/sendrecva.git
# git remote show origin
# (Replace aabbtree77 with your github username)

# python3 PCA_run.py readvals
# python3 PCA_run.py water
# python3 PCA_run.py thanks
# python3 PCA_run.py any garbage including empty string

def main():

    dict_A = {}
    dict_A["command"] = sys.argv[1]
    now = datetime.datetime.now()
    dict_A["date"] = now.strftime("%Y-%m-%d %H:%M:%S")
    PCA_send_pydict(dict_A)

    status = "Nothing Received"
    dict_B = {}
    result_values = ["Done reading.", 
                     "Done watering.", 
                     "Done detecting illegal.",
                     "End of the task, next please."]
    while status not in result_values:   
        print("Waiting 1800 sec.\n") 
        time.sleep(1800.0)    
        dict_B = PCA_recv_pydict(r'https://github.com/aabbtree77/sendrecvb.git')
        status = dict_B["status"]
        
    dict_A["command"] = "thanks"
    now = datetime.datetime.now()
    dict_A["date"] = now.strftime("%Y-%m-%d %H:%M:%S")
    PCA_send_pydict(dict_A)


def PCA_send_pydict(py_dict):
    
    json_formatted_str = json.dumps(py_dict, indent=4)

    print("Pushing this json file:\n") 
    print(json_formatted_str)
    with open('PCA_data.json', 'w+', encoding='utf-8') as fd:    
        fd.write(json_formatted_str)

    cmd = "git add PCA_data.json"
    subprocess.call(cmd, shell=True)
    cmd = 'git commit -m "my commit"'
    subprocess.call(cmd, shell=True)
    cmd = "git push origin main"
    subprocess.call(cmd, shell=True)
    

def PCA_recv_pydict(git_repo_b):

    cmd = "rm -rf temp" 
    subprocess.call(cmd, shell=True)
    cmd = "git clone " + git_repo_b + " temp" 
    subprocess.call(cmd, shell=True)
    
    py_dict = {}
    with open('temp/PCB_data.json', 'r', encoding='utf-8') as fd:
        py_dict = json.load(fd)
        
    json_formatted_str = json.dumps(py_dict, indent=4)   
    print("Received this json file:\n") 
    print(json_formatted_str)
    
    return py_dict


if __name__ == "__main__":
    main()
        
