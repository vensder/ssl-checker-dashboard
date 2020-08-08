#!/usr/bin/env python3.8

import schedule
import time
import ssl_checks as ssl
import redis
from multiprocessing.pool import ThreadPool as Pool
import hashlib
from os import environ
from distutils.util import strtobool

redis_host = "redis"
if "REDIS_HOST" in environ and environ["REDIS_HOST"]:
    redis_host = environ["REDIS_HOST"]

seconds_between_info_updates = 60 * 60 * 2
if (
    "SECONDS_BETWEEN_INFO_UPDATES" in environ
    and (environ["SECONDS_BETWEEN_INFO_UPDATES"]).isnumeric()
):
    seconds_between_info_updates = int(environ["SECONDS_BETWEEN_INFO_UPDATES"])

seconds_between_checks_for_outdating = 60 * 10
if (
    "SECONDS_BETWEEN_CHECKS_FOR_OUTDATING" in environ
    and (environ["SECONDS_BETWEEN_CHECKS_FOR_OUTDATING"]).isnumeric()
):
    seconds_between_checks_for_outdating = int(
        environ["SECONDS_BETWEEN_CHECKS_FOR_OUTDATING"]
    )

seconds_between_file_checks = 10
if (
    "SECONDS_BETWEEN_FILE_CHECKS" in environ
    and (environ["SECONDS_BETWEEN_FILE_CHECKS"]).isnumeric()
):
    seconds_between_file_checks = int(environ["SECONDS_BETWEEN_FILE_CHECKS"])

is_hash_sum_check_enabled = False
if "IS_HASH_SUM_CHECK_ENABLED" in environ:
    is_hash_sum_check_enabled = strtobool(environ["IS_HASH_SUM_CHECK_ENABLED"])

domains_file = "domains.lst"
domains_set = set()
default_domains = [
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
    "notexisting.domain",
]

r = redis.Redis(host=redis_host)


def domains_file_md5():
    try:
        with open(domains_file, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print("Exception during to open file", str(e))
        return 0


def update_domains_list_from_file():
    try:
        with open(domains_file, "r") as f:
            my_list = []
            domains = f.read().splitlines()
            for domain in domains:
                if str(domain).strip():
                    my_list.append(domain.strip())
        return my_list
    except Exception as e:
        print("Exception during to open domain list file", str(e))
        print("Using the default domain list")
        return default_domains


def is_redis_available():
    try:
        r.ping()
    except Exception as e:
        print("Redis is not available:", str(e))
        return False
    return True


def decode_redis_value(value):
    value = value.decode("utf-8")
    if value.isnumeric():
        value = int(value)
    return value


def update_all_domains_in_redis(domains_set):
    if is_redis_available():
        if len(domains_set) > 50:
            domains_chunk_size = int(len(domains_set) / 10)
        else:
            domains_chunk_size = len(domains_set)
        begin = 0
        while begin < len(domains_set):
            sub_set = set(list(domains_set)[begin : begin + domains_chunk_size])
            pool = Pool(len(sub_set))
            for result_tuple in pool.imap_unordered(
                ssl.tuple_domain_unixtime_expiration, sub_set
            ):
                if (not r.hget(result_tuple[0], "exp")) or (
                    round(time.time())
                    - decode_redis_value(r.hget(result_tuple[0], "updated"))
                    > seconds_between_info_updates
                ):
                    r.hset(
                        name=result_tuple[0],
                        mapping={"exp": result_tuple[1], "updated": round(time.time())},
                    )
            print("Updated info for domains: {}".format(str(sub_set)))
            time.sleep(1)
            begin += domains_chunk_size


def update_outdated_info_in_redis():
    if is_redis_available():
        from_redis_set = set()
        for domain in domains_set:
            if (not r.hget(domain, "exp")) or (
                round(time.time()) - decode_redis_value(r.hget(domain, "updated"))
                > seconds_between_info_updates
            ):
                from_redis_set.add(domain)
        if from_redis_set:
            update_all_domains_in_redis(from_redis_set)


def update_all_missing_domains_in_redis():
    from_redis_set = set()
    if is_redis_available():
        for key in r.keys("*"):
            from_redis_set.add(decode_redis_value(key))
    difference = domains_set - from_redis_set
    if difference:
        update_all_domains_in_redis(difference)


def update_domains_if_md5_changed():
    global md5_hash
    global domains_set
    md5_new = domains_file_md5()
    if md5_hash != md5_new:
        print("updating domains from file")
        domains_set = set(update_domains_list_from_file())
        update_all_missing_domains_in_redis()
        md5_hash = md5_new


if is_hash_sum_check_enabled:
    md5_hash = domains_file_md5()

domains_set = set(update_domains_list_from_file())

while not is_redis_available():
    print("Waiting for the Redis during the startup...")
    time.sleep(2)

update_all_domains_in_redis(domains_set)

if is_hash_sum_check_enabled:
    schedule.every(seconds_between_file_checks).seconds.do(
        update_domains_if_md5_changed
    )

schedule.every(seconds_between_checks_for_outdating).seconds.do(
    update_outdated_info_in_redis
)

while True:
    schedule.run_pending()
    time.sleep(1)
