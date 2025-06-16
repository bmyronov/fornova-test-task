![alt text](https://github.com/bmyronov/fornova-test-task/blob/main/media/diagram_task2_1.png?raw=true)

### Usage
- Rename `.env_example` to `.env` in *current folder*, *api folder* and in *test_runners folder*.

In `test_runner` env:
```
# test_runner
PLATFORMNAME=Android # Platforn you're gonna use e.g. 'Android'
PLATFORMVERSION=12 # Android version you're using
AUTOMATIONNAME=uiautomator2
DEVICENAME=HA1SL3H2 # Device id you can check it with 'adb devices'
APPPACKAGE=com.tripadvisor.tripadvisor # App id
# APPACTIVITY=.OnboardingActivity
LANGUAGE=en
HOST=your_ip_adress # Check it with Linux: ip a, Windows: ipconfig
PORT=4723
```
To ckeck your local ip adress on Linux use command: `ip a`. It will print something like this:
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether .... brd ff:ff:ff:ff:ff:ff
    altname ...
    inet 192.168.0.12/24 brd 192.168.0.255 scope global dynamic noprefixroute enp3s0
       valid_lft 81184sec preferred_lft 81184sec
    inet6 .... scope link noprefixroute 
```
`inet 192.168.0.12/24` is what you need. Your ip is `192.168.0.12`. Paste it to `.env` file.

On Windows type in cmd command `ipconfig`. It will print something like this:
```
...

Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : ...
   IPv4 Address. . . . . . . . . . . : 192.168.0.12
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.0.1

...
```
`Pv4 Address. . . . . . . . . . . : 192.168.0.12` is what you need. Your ip is `192.168.0.12`. Paste it to `.env` file.

- run `docker compose up -d`
- Go to http://127.0.0.1:8000/docs and run /search from there or use curl:
``` bash
curl -X 'GET' \
  'http://127.0.0.1:8000/search' \
  -H 'accept: application/json'
```
