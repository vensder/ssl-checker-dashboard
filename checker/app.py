#!/usr/bin/env python3

import schedule
import time
import ssl_checks as ssl
import redis
from multiprocessing.pool import ThreadPool as Pool
import hashlib
from os import environ
# from distutils.util import strtobool
from str_to_bool import str_to_bool as strtobool

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

is_first_load_from_file_enabled = False
if "IS_FIRST_LOAD_FROM_FILE_ENABLED" in environ:
    is_first_load_from_file_enabled = strtobool(
        environ["IS_FIRST_LOAD_FROM_FILE_ENABLED"]
    )


hosts_file = "hosts.lst"
hosts_set = set()

r = redis.Redis(host=redis_host)


def hosts_file_md5():
    try:
        with open(hosts_file, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print("Exception during to open file", str(e))
        return 0


def update_hosts_list_from_file():
    try:
        with open(hosts_file, "r") as f:
            my_list = []
            hosts = f.read().splitlines()
            for host in hosts:
                if str(host).strip():
                    my_list.append(host.strip())
        return my_list
    except Exception as e:
        print("Exception during to open host list file", str(e))
        return []


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


def update_all_hosts_in_redis(hosts_set):
    if is_redis_available() and hosts_set:
        if len(hosts_set) > 50:
            hosts_chunk_size = int(len(hosts_set) / 10)
        else:
            hosts_chunk_size = len(hosts_set)
        begin = 0
        while begin < len(hosts_set):
            sub_set = set(list(hosts_set)[begin : begin + hosts_chunk_size])
            pool = Pool(len(sub_set))
            for result_tuple in pool.imap_unordered(
                ssl.tuple_host_unixtime_expiration, sub_set
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
            print("Updated info for hosts: {}".format(str(sub_set)))
            time.sleep(1)
            begin += hosts_chunk_size


def update_outdated_info_in_redis():
    if is_redis_available():
        from_redis_set = set()
        for host in hosts_set:
            if (not r.hget(host, "exp")) or (
                round(time.time()) - decode_redis_value(r.hget(host, "updated"))
                > seconds_between_info_updates
            ):
                from_redis_set.add(host)
        if from_redis_set:
            update_all_hosts_in_redis(from_redis_set)


def sync_hosts_with_redis():
    from_redis_set = set()
    if is_redis_available():
        for key in r.keys("*"):
            from_redis_set.add(decode_redis_value(key))
    difference = hosts_set - from_redis_set
    if difference:
        update_all_hosts_in_redis(difference)
    difference = from_redis_set - hosts_set
    if difference:
        r.delete(*difference)


def update_hosts_if_md5_changed():
    global md5_hash
    global hosts_set
    md5_new = hosts_file_md5()
    if md5_hash != md5_new:
        print("updating hosts from file")
        hosts_set = set(update_hosts_list_from_file())
        sync_hosts_with_redis()
        md5_hash = md5_new


if is_hash_sum_check_enabled:
    md5_hash = hosts_file_md5()

if is_first_load_from_file_enabled:
    hosts_set = set(update_hosts_list_from_file())

while not is_redis_available():
    print("Waiting for the Redis during the startup...")
    time.sleep(2)

update_all_hosts_in_redis(hosts_set)

if is_hash_sum_check_enabled:
    schedule.every(seconds_between_file_checks).seconds.do(
        update_hosts_if_md5_changed
    )

schedule.every(seconds_between_checks_for_outdating).seconds.do(
    update_outdated_info_in_redis
)

while True:
    schedule.run_pending()
    time.sleep(1)
