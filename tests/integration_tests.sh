#!/usr/bin/env bash

set -e -x

remove_all_containers () {
  docker-compose -f docker-compose-test.yml stop -t 0
  docker-compose -f docker-compose-test.yml rm -f
}

build_images () {
  docker-compose -f docker-compose-test.yml build "$@"
}

up_containers () {
  docker-compose -f docker-compose-test.yml up -d "$@"
}

list_all_containers () {
  docker-compose -f docker-compose-test.yml ps
}

logs_containers () {
  docker-compose -f docker-compose-test.yml logs "$@"
}

test_webapp () {
  curl localhost:8080 | grep href
  curl -s -o /dev/null -w "%{http_code}" localhost:8080/health | grep 200
  curl -s localhost:8080 | grep 'google.com'
  curl -s localhost:8080/all | grep 'google.com'
  curl -s localhost:8080/days | grep 'google.com'
  curl -s localhost:8080/errors | grep 'notexisting.domain'
}

get_redis_keys () {
  docker-compose -f docker-compose-test.yml exec -T redis redis-cli --scan
}

remove_all_containers
cp tests/domains_small.lst cron/domains.lst
build_images "cron"
up_containers "redis" "cron"
sleep 5
list_all_containers
logs_containers "redis" "cron"
get_redis_keys
up_containers "web-app"
sleep 2
list_all_containers
logs_containers "web-app"

test_webapp

docker cp tests/domains_medium.lst ssl-checker-dashboard_cron_1:/home/app/domains.lst
sleep 30
list_all_containers
logs_containers "cron"
get_redis_keys

test_webapp

remove_all_containers

git checkout -- cron/domains.lst
build_images "cron"

up_containers "redis" "cron"
sleep 40
list_all_containers
logs_containers "redis" "cron"
get_redis_keys
up_containers "web-app"
sleep 10

list_all_containers
test_webapp
remove_all_containers