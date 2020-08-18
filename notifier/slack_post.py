from os import environ
import urllib.request
import json


webhook_url = ""

if "WEBHOOK_URL" in environ and environ["WEBHOOK_URL"]:
    webhook_url = environ["WEBHOOK_URL"]


def compose_message(hosts_days_dict):
    message_text = ""
    for host in hosts_days_dict:
        message_text += f"\nThe SSL certificate of {host} will expire in {hosts_days_dict[host]} day(s)"
    return message_text

def post_message(webhook_url, hosts_days_dict):
    if not webhook_url:
        raise Exception("Empty webhook url")
    data = {
        "text": compose_message(hosts_days_dict),
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
