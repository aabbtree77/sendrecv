## Introduction

This is a memo which documents a way to send messages from computer to computer via the internet.
The idea is to avoid complicated setups and protocols and rely on "git push" and "git clone" provided by github.com as a free 3rd party service.

*Warning 1. "git push" and "git clone" require a manual initial setup for each "peer" machine. This is also a very raw code and strictly a prototype for slow messaging as the code will incrementally flood your github folder history with each file update. As an example, communicating a json object with a few elements every 30 minutes has increased my .git folder by 60KB in 5 days. Thus, exchanging a single value message every 10s. between two peers for a month will yield two .git folders each as large as roughly 60KBx30x6x6=65MB. A year of such a continuous communication is likely to exceed your free github user quota.*

*Warning 2. IPFS could be a much better way to implement a simple file-based communication accessible globally. However, it is not clear if the specific IPFS implementation will always expose every node behind any NAT configuration, while this silly-looking way will **ALWAYS** work irrespectively of the network configuration as long as github.com is online.* 

## Problem/Motivation

How do you send messages from a computer PC-A to a computer PC-B globally, via the internet, without a pain? 
Imagine the situation not so atypical to the embedded software: One needs to control a remote board (which communicates with some PC-A on its LAN) from some PC-B (located outside 
of the LAN).

The messages can be small text commands, they can be open/visible to anyone, but only PC-A and PC-B can send them. The messages may arrive slowly, in seconds or minutes.

An example application is monitoring temperature of a greenhouse and watering its plants remotely.

Locally, the MQTT protocol with the Mosquitto broker on Ubuntu is a solid answer, but this option does not extend globally.

It is assumed that both of the computers run Linux and have access to the internet, but port forwarding is broken. Having RDC/ssh is too much, the computers simply run Python programs which depend on the messages they receive.

One can work out a VPN solution based on [Wireguard or go-libp2p](https://github.com/aabbtree77/esp32-mqtt-experiments#congratulations-you-had-a-problem-and-now-you-have-two) depending on whether one has a public static IP or not, resp. However, this requires quite some search and experimenting with network setups designed for much bigger tasks such as the ability to create multi-purpose networks, access the whole remote OS via ssh or even RDC, when the problem at hand is just sending a simple text message to a remote machine.

The idea here is to communicate by uploading json files to any peer's github repo and cloning the others in the "read only" mode.

In order not to have pushing conflicts when a remote branch is already updated, let's use one github repo per peer/client/server which will also be duplicated: Every peer will have its remote git "origin" (say on github.com) and local "main" (peer's PC or even Android).

An example code deserves a brief description:

0. The subfolders "sendrecva" and "sendrecvb" must first be set up on github as independent ordinary repos with their initial .git subfolders.

1. The repo "sendrecva" is initially cloned to the computer PC-A with its git remote origin configured aftwerwards with the corresponding access token. This computer will later only "git push" to its remote branch, no "git fetch" or "git pull" will ever take place.
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

The downside of this approach is that each peer/communicating node needs to register on github.com first, create a repo, set its access token. Thus, the end user of such a communication would be, say, a Python coder who wants to make his LAN nodes global by sending messages from PC to PC via the internet, in code, without having to deal with anything other than github.com. I find setting up and testing my github repositories a lot easier and more reliable than dealing with any 3rd party MQTT broker or remote desktop software.

## Inspiration, Alternatives, Deeper Ideas

[using-git-repository-as-a-database-backend](https://stackoverflow.com/questions/20151158/using-git-repository-as-a-database-backend)

[git-nosql-database](https://www.kenneth-truyers.net/2016/10/13/git-nosql-database/)

[nat-traversal-github-actions-openvpn-wireguard](https://github.com/ValdikSS/nat-traversal-github-actions-openvpn-wireguard)   
