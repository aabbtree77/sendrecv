# Problem

How do you send messages from a computer A to a computer B globally via internet without a pain? 
Imagine a situation typical in the embedded world. One needs to control some remote board which communicates with some PC-A on its LAN, from some PC-B located outside 
of the LAN.

The messages can be small text commands, they can be open/visible to anyone, but only PC-A and PC-B can send them. The messages may arrive slowly, in seconds or minutes.

An example application is monitoring a green house and watering plants remotely.

Locally, the MQTT protocol with the Mosquitto broker is a solid answer, but this option does not extend globally.

One gets tired of dealing with router configurations, ssh, tunneling, Ubuntu, Wayland vs X11, VNC, RDP, MQTT, Remmina, TeamViewer, AnyDesk, CloudMQTT, HiveMQ, RustDesk, UDP and TCP hole punching, p2p torrents.

One option is to use gmail or github, and this code is the demo of using the latter.  

The idea is to communicate by uploading json files to a github repo.

In order not to have pushing conflicts when a remote branch is already updated one sets up two github repos.

1. A repo "sendrecva" is initially cloned to the computer PC-A. This computer will later only push the code to its remote branch, no git fetch or pull will ever take place.
  To get data, PC-A clones a json file from "sendrecvb" into its temp folder, reads the keys and values and deletes the temp folder.
  
2. Similarly with "sendrecvb" which will only push to its remote branch and will read via "git clone sendrecvb temp".

3. PC-A: execute "python3 PCA_run.py readvals" in the terminal.

4. PC-B: execute "python3 PCB_run.py".

Sometimes if the program is halted with ctrl+C or you start modifying code remotely, or something goes out of sync initially:

  - rm -rf temp 
  - git pull origin main --rebase
  - git add .
  - git commit -m "my commit"
  - git push origin main
  
Notice that there is no "git fetch" or "git pull" inside code, only "git clone", which is critical to automation and avoiding conflicts.


References (Inspiration, Alternatives, Deeper and More Complex Ideas)

[using-git-repository-as-a-database-backend](https://stackoverflow.com/questions/20151158/using-git-repository-as-a-database-backend)
[git-nosql-database](https://www.kenneth-truyers.net/2016/10/13/git-nosql-database/)
   
