#!/bin/env python3

# NB: this requires 'graphviz' to be installed on the system (e.g. via apt)

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.network import Nginx
from diagrams.generic.blank import Blank
from diagrams.onprem.client import Client, User
# from urllib.request import urlretrieve

CONN_COLOR = 'dodgerblue4'

with Diagram("",
             show=False,
             filename="diagram",
             direction="LR",
             node_attr={"fontsize": "15", "height": "1.1", "width": "1.1"},
             edge_attr={'penwidth': '2'},
             graph_attr={'pad': '0.5'},
             curvestyle="curved"):

  player = Client("Player")
  admin = User("Admin")

  # download the icon image file
  with Cluster("AWS EC2 instance (t3.small)", direction="LR"):

    with Cluster("UT2004 dedicated server process") as dedicated_server:

      # ut2004_url = "https://media.moddb.com/cache/images/downloads/1/263/262036/thumb_620x2000/Unreal_Tournament_2004_HD_Icon.png"
      # ut2004_icon = "img/ut2004.png"
      # urlretrieve(ut2004_url, ut2004_icon)
      ut = Custom("Game server", "img/ut2004.png")
      ut_webadmin = Custom("Web admin\nHTTP server", "img/ut2004.png")

    nginx = Nginx("Nginx\nreverse proxy")
    nginx >> Edge(color=CONN_COLOR, headlabel='\n8075', fontsize='15', labelfontcolor=CONN_COLOR) >> ut_webadmin

    # f2b_url = "https://upload.wikimedia.org/wikipedia/commons/d/db/Fail2ban_logo.png"
    # f2b_icon = "img/f2b.png"
    # urlretrieve(f2b_url, f2b_icon)
    f2b = Custom("Fail2ban", "img/f2b.png")

    nginx >> f2b

    # netfilter_url = "https://wiki.nftables.org/wiki-nftables/netfilter-mini-flame.png?02eb9"
    # netfilter_icon = "img/nftables.png"
    nftables = Custom("Netfilter\n(nftables/iptables)", "img/netfilter.png")

    # nftables >> nginx
    # nftables >> ut
    nftables << f2b

    ufw = Custom("UFW", "img/ufw.png")
    nftables << ufw

    lgsm = Custom("\n\nLinuxGSM", "img/linuxgsm.png")
    ut << lgsm
    ut_webadmin << lgsm

    cron = Custom("Cron jobs", "img/cron.png")
    lgsm << cron

    noip_duc = Custom("No-IP DUC", "img/noip.png")

  noip = Custom("No-IP DNS server", "img/noip.png")
  noip << noip_duc

  player >> Edge(color=CONN_COLOR, headlabel='\n7777', fontsize='15', labelfontcolor=CONN_COLOR) >> ut
  admin >> Edge(color=CONN_COLOR, headlabel='\n80', fontsize='15', labelfontcolor=CONN_COLOR) >> nginx

  player >> noip
  admin >> noip