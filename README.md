## Introduction

This is a memo which documents a way to send messages from computer to computer via internet.
The idea is to avoid complicated setups and protocols and rely on "git push" and "git clone" provided by Github as a free 3rd party service.

An example "server"/"client" code can be found in these repositories:

  - [Code to be cloned to PC-A](https://github.com/aabbtree77/sendrecva).
  
  - [Code to be cloned to PC-B](https://github.com/aabbtree77/sendrecvb).

## Problem/Motivation

How do you send messages from a computer A to a computer B globally, via the Internet, without a pain? 
Imagine the situation not so atypical to the embedded software: One needs to control a remote board (which communicates with some PC-A on its LAN) from some PC-B (located outside 
of the LAN).

The messages can be small text commands, they can be open/visible to anyone, but only PC-A and PC-B can send them. The messages may arrive slowly, in seconds or minutes.

An example application is monitoring temperature of a greenhouse and watering its plants remotely.

Locally, the MQTT protocol with the Mosquitto broker on Ubuntu is a solid answer, but this option does not extend globally.

One gets tired of dealing with router configurations, ssh, tunneling, firewalls, version changes, Wayland vs X11, VNC, RDP, MQTT, Remmina, TeamViewer, AnyDesk, CloudMQTT, HiveMQ, RustDesk, UDP and TCP hole punching, p2p torrents. If you are lucky, you can do a simple port forwarding in your router and use a slowly changing global IP and the port number to connect to any computer globally with Remmina, but that seems to work only with certain ISP NAT configurations. In general, one needs a reliable 3rd party service to communicate on the web, preferably free and also hassle-free.

There are not that many choices. A mail service comes to mind, but also github, and this code is the demo of using the latter.  

The idea is to communicate by uploading json files to any peer's github repo and cloning the others in the "read only" mode thus exchanging Python dictionaries/Json objects.

In order not to have pushing conflicts when a remote branch is already updated, let's use one github repo per peer/client/server which will be duplicated on remote "origin" (github) and local "main" (peer's PC).

An example code deserves a brief description:

1. The repo "sendrecva" is initially cloned to the computer PC-A. This computer will later only "git push" to its remote branch, no "git fetch" or "git pull" will ever take place.
  To get data, PC-A clones the PCB_data.json file from "sendrecvb" into its temp folder, reads the keys and values and deletes the "temp" folder so that the next "git clone" to the same "temp" folder becomes available.
  
2. Similarly with "sendrecvb" on PC-B which will only push to its remote branch and will read via "git clone sendrecva temp".

3. PC-A: execute "python3 PCA_run.py readvals" in the terminal.

4. PC-B: execute "python3 PCB_run.py".

If the program is halted with ctrl+C or you start modifying code remotely, or something goes out of sync initially:

  - rm -rf temp 
  - git pull origin main --rebase
  - git add .
  - git commit -m "my commit"
  - git push origin main
  
Notice that there is no "git fetch" or "git pull" inside the codes, only "git clone", which is critical to automation and avoiding conflicts. The latter can only appear during the initial setup or restart after some remote code modifications.

The downside of this approach is that each peer/communicating node needs to register on github.com first, create a repo, set up its access token. Thus, the end user of such a communication would be, say, a Python coder who wants to make his LAN nodes global by sending messages from PC to PC via the Internet, in code, without having to deal with anything other than github.com. I find setting up and testing my github repositories a lot easier and more reliable than dealing with any 3rd party MQTT broker or remote desktop software.

## References (Inspiration, Alternatives, Deeper and More Complex Ideas)

[using-git-repository-as-a-database-backend](https://stackoverflow.com/questions/20151158/using-git-repository-as-a-database-backend)

[git-nosql-database](https://www.kenneth-truyers.net/2016/10/13/git-nosql-database/)
   
