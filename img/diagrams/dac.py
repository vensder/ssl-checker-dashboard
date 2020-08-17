#!/usr/bin/env python

from diagrams import Diagram, Cluster
from diagrams.aws.network import ELB
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Internet, Nginx
from diagrams.saas.chat import Slack
from diagrams.onprem.compute import Server
from diagrams.onprem.client import User


graph_attr = {"fontsize": "18", "pad": "0"}

with Diagram(
    "SSL Checker Dashboard Diagram",
    filename="ssl-checker-diagram",
    show=False,
    graph_attr=graph_attr,
):
    user = User("User")
    ingress = Nginx("ingress")

    with Cluster("Dashboard Replicas"):
        dashboards = [
            Docker("dashboard"),
            Docker("dashboard"),
            Docker("dashboard"),
        ]

    checker = Docker("checker")

    notifier = Docker("notifier")

    user >> ingress >> dashboards >> Redis("redis") << [checker, notifier]

    checker >> Internet("hosts with SSL")
    notifier >> Slack("Slack")
