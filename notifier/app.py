#!/usr/bin/env python3

import schedule
import time
from slack_post import webhook_url, post_message


def send_info():
    if webhook_url:
        response_code = post_message(webhook_url, "example.com", 5)
        print(response_code)


if __name__ == "__main__":
    schedule.every(2).seconds.do(send_info)
    while True:
        schedule.run_pending()
        time.sleep(1)
