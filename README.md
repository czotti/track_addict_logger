This script watch a logfile and push the data to a NBP client like TrackAddict.

# Installation base system
You need:
- [python3](https://www.python.org/download/releases/3.0/)
- virtualenv to install package locally
- pip
- [git](https://git-scm.com/)

In ubuntu like system:
```
sudo apt install python3 python3-pip python3-virtualenv
```

In windows well have fun :p ([anaconda](https://www.anaconda.com/distribution/) should be a good option)

# Environment
Clone the repository
```
git clone https://github.com/czotti/track_addict_logger.git
cd track_addict_logger
```

Prepare the environment:
```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

# Usage
Prior to start the script you need to find the IP.
```
$ ip addr
https://github.com/czotti/track_addict_logger.git1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s25: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 54:ee:75:41:41:bf brd ff:ff:ff:ff:ff:ff
3: wlp4s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 0c:9d:92:b6:43:5d brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.163/24 brd 10.140.255.255 scope global dynamic noprefixroute wlp0s20u1
       valid_lft 4098sec preferred_lft 4098sec
    inet6 fe80::703e:13ad:1d49:e4b4/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```

Here the ip of the interface connected to my network is: `192.168.1.163`.

You are ready to start the script.
```
source .venv/bin/activate
python3 notify.py /path/to/the/logfile.msl -ip 192.168.1.163 
```

After this pynbp should log some message in the command line.
Be sure to have a clean log file before running the script because it will push the old data to the client (maybe remove this behavior?).

To close the script simply press `CTRL+C`.