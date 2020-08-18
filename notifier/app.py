#!/usr/bin/env python3

import schedule
import time
from slack_post import webhook_url, post_message
import redis
from os import environ
from datetime import datetime
from distutils.util import strtobool


redis_host = "redis"
if "REDIS_HOST" in environ and environ["REDIS_HOST"]:
    redis_host = environ["REDIS_HOST"]

# days_before_to_notify
# days_left_to_notify
notify_if_days_left = 30
if "NOTIFY_IF_DAYS_LEFT" in environ and environ["NOTIFY_IF_DAYS_LEFT"]:
    notify_if_days_left = int(environ["NOTIFY_IF_DAYS_LEFT"])

notify_every_n_hours = 0.5
if "NOTIFY_EVERY_N_HOURS" in environ and environ["NOTIFY_EVERY_N_HOURS"]:
    notify_every_n_hours = float(environ["NOTIFY_EVERY_N_HOURS"])


def send_notification(host, days):
    response_code = post_message(webhook_url, host, days)
    return response_code


def is_redis_available():
    try:
        r.ping()
    except Exception as e:
        print("Redis is not available:", str(e))
        return False
    return True


def notify_expiring_soon():
    if is_redis_available():
        for host in r.keys("*"):
            if r.hget(host, "exp"):
                host = host.decode("utf-8")
                expire_unix_time = r.hget(host, "exp").decode("utf-8")
                if expire_unix_time.isnumeric():
                    seconds_left = int(expire_unix_time) - datetime.now().timestamp()
                    if seconds_left <= notify_if_days_left * 86400:
                        days_left = seconds_left // 86400
                        if not r.hget(host, "notified") or not strtobool(
                            r.hget(host, "notified").decode("utf-8")
                        ):
                            print(
                                f"SSL cert of {host} will expire in {days_left} day(s)"
                            )
                            send_notification(host, days_left)
                            r.hset(host, "notified", "True")


def delete_notified_mark():
    if is_redis_available():
        for host in r.keys("*"):
            if r.hget(host, "notified"):
                r.hset(host, "notified", "False")


if __name__ == "__main__":
    r = redis.Redis(host=redis_host)

    schedule.every(10).seconds.do(notify_expiring_soon)
    schedule.every(notify_every_n_hours).hours.do(delete_notified_mark)
    while True:
        schedule.run_pending()
        time.sleep(1)
