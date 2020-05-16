# FritzOver-Gateway
FritzOver-Gateway is a python script, which changes the default route of a specific NIC if FritzBox fails link or ping.
I wrote this script because of my current ISP situation: My ISP currently does some maintenance and the connection drops for a few hours a day. Luckily, I've got a ThinkPad x230 with an UMTS module set up in my LAN. If the conneciton over fritzbox fails, the script changes the default gateway to my x230. :shipit:

### Tech

FritzOver-Gateway uses following open-source projects:

* [fritzconnection](https://github.com/kbr/fritzconnection) - Python-Tool to communicate with the AVM FritzBox

### Setup
Edit the default values in the script or use env-variables.
| ENV | DESC |
| ------ | ------ |
| `FO_PING_HOST` | Host used for test-pings. |
| `FRITZBOX_GATEWAY` | address of the fritzbox |
| `FAILOVER_GATEWAY` | gateway to use if fritzbox fails |
| `FO_INTERFACE` | interface used within the fritzbox LAN |
| `FRITZBOX_PASSWORD` | password used to log into fritzbox's web-interface |

License
----

[MIT](LICENSE.txt)
