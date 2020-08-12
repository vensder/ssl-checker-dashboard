#!/usr/bin/env python

from diagrams import Diagram
from diagrams.aws.network import ELB
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Internet

graph_attr = {
    "fontsize": "18",
    "pad": "0"
}

with Diagram("ssl-checker-diagram", show=False, graph_attr=graph_attr):
    Internet("Internet") >> ELB("ingress") >> [
            Docker("dashboard"), 
            Docker("dashboard"),
            Docker("dashboard")
            ] >> Redis("redis") << Docker("checker")


