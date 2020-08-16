from os import environ
import urllib.request
import json


webhook_url = ""

if "WEBHOOK_URL" in environ and environ["WEBHOOK_URL"]:
    webhook_url = environ["WEBHOOK_URL"]


def post_message(webhook_url, host, days):
    if not webhook_url:
        raise Exception("Empty webhook url")
    data = {
        "text": f"The SSL certificate of {host} will expire in {days} day(s)",
        "username": "SSL-notifier",
        "icon_emoji": ":robot_face:",
    }
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req)
        return resp.getcode()
    except Exception as e:
        print("Exception due to send message to slack:", str(e))
        return str(e)
