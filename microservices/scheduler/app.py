#!/usr/bin/env python3.8

import schedule
import time
import ssl_checks as ssl
import redis
from multiprocessing.pool import ThreadPool as Pool


try:
    with open("domains.lst") as f:
        domains = f.read().splitlines()
except Exception as e:
    print("Exception during to open domain list file", str(e))
    print("Using the default domain list")
    domains = [
        "aws.amazon.com",
        "google.com",
        "yandex.ru",
        "google.com",
        "youtube.com",
        "linkedin.com",
        "github.com",
        "ubuntu.com",
        "debian.org",
        "linuxmint.com",
        "linkedin.com",
        "microsoft.com",
        "google.com",
        "linux.org.ru",
        "meduza.io",
        "echo.msk.ru",
        "example.com",
        "github.com",
        "flw.im",
        "o-nix.com",
        "kubernetes.io",
        "cloud.google.com",
        "python.org",
        "docs.python.org",
        "wikipedia.org",
        "en.wikipedia.org",
        "bottlepy.org",
        "hub.docker.com",
        "docker.com",
        "pypi.org",
        "stackoverflow.com",
        "realpython.com",
        "medium.com",
        "linux.org",
    ]


domains_set = set(domains)
domains_days_set = set()

r = redis.Redis(host='redis')


def is_redis_available():
    try:
        r.ping()
    except Exception as e:
        print("Redis is not available:", str(e))
        return False
    return True


def update_all_domains_in_redis(domains_set):
    pool = Pool(len(domains_set))
    for result_tuple in pool.imap_unordered(ssl.tuple_domain_days_before_expiration, domains_set):
        if not r.get(result_tuple[0]):
            r.set(result_tuple[0], result_tuple[1])


def update_all_missing_domains_in_redis():
    from_redis_set = set()

    if is_redis_available():
        for key in r.keys('*'):
            from_redis_set.add(key.decode('utf-8'))

    difference = domains_set - from_redis_set
    if (difference):
        update_all_domains_in_redis(difference)


update_all_missing_domains_in_redis()

schedule.every(5).seconds.do(update_all_missing_domains_in_redis)


while True:
    schedule.run_pending()
    time.sleep(1)
