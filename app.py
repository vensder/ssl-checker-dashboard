#!/usr/bin/env python3.8

from bottle import route, run, hook, request, default_app, TEMPLATE_PATH, template, static_file
from datetime import datetime
import redis

domains_days_dict = dict()

r = redis.Redis()


def is_redis_available():
    try:
        r.ping()
    except Exception as e:
        print("Redis is not available:", str(e))
        return False
    return True


def get_all_from_redis():
    if is_redis_available():
        for key in r.keys('*'):
            info = r.get(key).decode('utf-8')
            if info.isnumeric() or type(info) is int:
                info = round((int(info) - datetime.now().timestamp())/86400)
            domains_days_dict[key.decode('utf-8')] = info


def get_info_from_set(domains_set, info_type):
    """
    Returns the set of tupples with domain name and days or errors.

    Args:
        domains_set (set): A set from domain names (str)
        info_type (str): A type of returning info ("days" or "errors")

    Returns:
        output_set (set): The set of tupples (domain(str), days(int)) or
        (domain(str), error(str))
    """
    if info_type == "days":
        return set(((a, b)) for (a, b) in domains_set if type(b) is int)
    elif info_type == "errors":
        return set(((a, b)) for (a, b) in domains_set if type(b) is str)


def get_info_from_dict(domains_dict, info_type):
    """
    Returns the set of tupples with domain name and days or errors.

    Args:
        domains_set (set): A set from domain names (str)
        info_type (str): A type of returning info ("days" or "errors")

    Returns:
        output_set (set): The set of tupples (domain(str), days(int)) or
        (domain(str), error(str))
    """
    if info_type == "days":
        my_dict = dict()
        for item in domains_dict:
            if type(domains_dict[item]) is int:
                my_dict[item] = domains_dict[item]
        return my_dict
    elif info_type == "errors":
        my_dict = dict()
        for item in domains_dict:
            if type(domains_dict[item]) is str:
                my_dict[item] = domains_dict[item]
        return my_dict


get_all_from_redis()


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
    if not domains_days_dict and is_redis_available():
        get_all_from_redis()
    return template(
        'domains',
        domains_days=domains_days_dict,
        refresh=0)


@route('/errors')
@route('/bad')
def show_hosts():
    if not domains_days_dict and is_redis_available():
        get_all_from_redis()
    return template(
        'domains',
        domains_days=get_info_from_dict(
            domains_dict=domains_days_dict, info_type="errors"),
        refresh=0)


@route('/days')
@route('/good')
def show_hosts():
    if not domains_days_dict and is_redis_available():
        get_all_from_redis()
    return template(
        'domains',
        domains_days=get_info_from_dict(
            domains_dict=domains_days_dict, info_type="days"),
        refresh=0)

# TODO: add sorted by days to expire


# Run bottle internal test server when invoked directly ie: non-uxsgi mode
if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)

# Run bottle in application mode.
# Required in order to get the application working with WSGI
else:
    app = application = default_app()
