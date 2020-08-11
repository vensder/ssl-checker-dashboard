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

with Diagram("SSL-checker-diagram", show=False, graph_attr=graph_attr):
    Internet("Internet") >> ELB("ingress") >> [
            Docker("web-app"), 
            Docker("web-app"),
            Docker("web-app")
            ] >> Redis("redis") << Docker("cron")


