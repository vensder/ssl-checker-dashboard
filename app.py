#!/usr/bin/env python3

from ssl_checks import days_before_expiration
from bottle import route, run, hook, request, default_app, TEMPLATE_PATH, template, static_file
from multiprocessing.pool import ThreadPool as Pool

import redis

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
use_redis = False
r = redis.Redis()


def is_redis_available():
    try:
        r.ping()
    except Exception as e:
        print("Redis is not available:", str(e))
        return False
    return True


def update_domains_days_in_set(domains_set):
    pool = Pool(len(domains_set))
    for result_tuple in pool.imap_unordered(days_before_expiration, domains_set):
        domains_days_set.add(result_tuple)


def update_domains_days_in_redis(domains_set):
    pool = Pool(len(domains_set))
    for result_tuple in pool.imap_unordered(days_before_expiration, domains_set):
        r.set(result_tuple[0], result_tuple[1])


def get_info_from_redis(domains_set, info_type="all"):
    """
    Returns the set of tupples with domain name and days or errors.

            Parameters:
                    domains_set (set): A set from domain names (str)
                    info_type (str): A type of returning info ("all", "days" or "errors")

            Returns:
                    output_set (set): The set of tupples (domain(str), days(int)) or
                        (domain(str), error(str)) or both in second element of set

    """
    output_set = set()
    for domain in domains_set:
        info = r.get(domain).decode("utf-8")
        if info_type == "days" and not info.isnumeric():
            continue
        if info_type == "errors" and info.isnumeric():
            continue
        if info.isnumeric():
            info = int(info)
        output_set.add((domain, info))
    return output_set


use_redis = is_redis_available()


if use_redis:
    for domain in domains_set:
        if not r.get(domain):
            update_domains_days_in_redis(domains_set)
else:
    update_domains_days_in_set(domains_set)


TEMPLATE_PATH[:] = ['templates']  # add a directory to template path
DEBUG = 0


@hook('before_request')  # hook to strip the trailing slashes
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


@route('/static/:path#.+#', name='static')  # for static files like css
def static(path):
    return static_file(path, root='static')


@route('/')
@route('/all')
@route('/hosts')
@route('/domains')
def show_hosts():
    if use_redis:
        domains_info = get_info_from_redis(domains_set, info_type="all")
    else:
        domains_info = domains_days_set
    return template(
        'domains',
        rows=sorted(domains_info),
        refresh=0)


@route('/errors')
def show_hosts():
    if use_redis:
        domains_info = get_info_from_redis(domains_set, info_type="errors")
    else:
        domains_info = domains_days_set
    return template(
        'domains',
        rows=sorted(domains_info),
        refresh=0)


@route('/days')
def show_hosts():
    if use_redis:
        domains_info = get_info_from_redis(domains_set, info_type="days")
    else:
        domains_info = domains_days_set
    return template(
        'domains',
        rows=sorted(domains_info),
        refresh=0)


# Run bottle internal test server when invoked directly ie: non-uxsgi mode
if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)

# # Run bottle in application mode.
# # Required in order to get the application working with uWSGI!
# else:
#     app = application = default_app()
