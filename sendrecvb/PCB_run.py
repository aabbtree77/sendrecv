import subprocess
import json
import time
import sys
import datetime

# This code is part of an experiment where two computers
# communicate via github. It is to be executed on the computer B:
# inside a properly git cloned and token-setup git repo "sendrecvb".

# One must have two github repos on the github server and their clones on the resp. machines
# with GITHUB_ACCESS_TOKEN set inside resp. bash files as indicated in http://www.compciv.org/recipes/devops/git-and-github-setup/
# git remote rm origin
# git remote add origin https://aabbtree77:$GITHUB_ACCESS_TOKEN@github.com/aabbtree77/sendrecvb.git
# git remote show origin
# (Replace aabbtree77 with your github username)

# python3 PCB_run.py

def main():

    dict_A = {}
    while True:
        
        dict_A = PCB_recv_pydict(r'https://github.com/aabbtree77/sendrecva.git')
        command = dict_A["command"]
        
        dict_B = {}    
        if command == "readvals":
            dict_B["temperature"] = "77"
            dict_B["status"] = "Done reading."
        elif command == "water":
            dict_B["status"] = "Done watering."
        elif command == "thanks":
            dict_B["status"] = "End of the task, next please."    
        else:
            dict_B["status"] = "Done detecting illegal."

        now = datetime.datetime.now()     
        dict_B["date"] = now.strftime("%Y-%m-%d %H:%M:%S")     
        
        PCB_send_pydict(dict_B)      
	                
        print("Waiting 10 sec.\n") 
        time.sleep(10.0)
    
    
def PCB_send_pydict(py_dict):
    
    json_formatted_str = json.dumps(py_dict, indent=4)

    print("Pushing this json file:\n") 
    print(json_formatted_str)
    with open('PCB_data.json', 'w+', encoding='utf-8') as fd:    
        fd.write(json_formatted_str)

    cmd = "git add PCB_data.json"
    subprocess.call(cmd, shell=True)
    cmd = 'git commit -m "my commit"'
    subprocess.call(cmd, shell=True)
    cmd = "git push origin main"
    subprocess.call(cmd, shell=True)
    

def PCB_recv_pydict(git_repo_a):
    
    cmd = "rm -rf temp" 
    subprocess.call(cmd, shell=True)
    cmd = "git clone " + git_repo_a + " temp" 
    subprocess.call(cmd, shell=True)
    
    py_dict = {}
    with open('temp/PCA_data.json', 'r', encoding='utf-8') as fd:
        py_dict = json.load(fd)
        
    json_formatted_str = json.dumps(py_dict, indent=4)   
    print("Received this json file:\n") 
    print(json_formatted_str)
 
    return py_dict
    
if __name__ == "__main__":
    main()      
