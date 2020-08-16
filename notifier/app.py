#!/usr/bin/env python3

from os import environ
import urllib.request
import json
import schedule
import time


webhook_url = ""

if "WEBHOOK_URL" in environ and environ["WEBHOOK_URL"]:
    webhook_url = environ["WEBHOOK_URL"]


def post_message(webhook_url, host, days):
    data = {
        "text": f"The SSL certificate of the {host} host will expire in {days} days",
        "username": "SSL-notifier",
        "icon_emoji": ":robot_face:",
    }
    req = urllib.request.Request(
        webhook_url, data=json.dumps(data).encode('utf-8'), headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req)
    return resp.getcode()


def send_info():
    if webhook_url:
        response_code = post_message(webhook_url, "example.com", 5)
        print(response_code)


if __name__ == "__main__":
    schedule.every(2).seconds.do(send_info)
    while True:
        schedule.run_pending()
        time.sleep(1)

