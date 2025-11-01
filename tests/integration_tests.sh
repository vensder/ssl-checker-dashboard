#!/usr/bin/env bash

set -e -x

remove_all_containers () {
  docker compose -f docker-compose-test.yml stop -t 0
  docker compose -f docker-compose-test.yml rm -f
}

build_images () {
  docker compose -f docker-compose-test.yml build "$@"
}

up_containers () {
  docker compose -f docker-compose-test.yml up -d "$@"
}

list_all_containers () {
  docker compose -f docker-compose-test.yml ps
}

logs_containers () {
  docker compose -f docker-compose-test.yml logs "$@"
}

test_dashboard () {
  curl -s localhost:8080/health | grep 'ok'
  curl -s localhost:8080/health | grep '"redis_available": "True"'
  curl -s localhost:8080 | grep href
  curl -s -o /dev/null -w "%{http_code}" localhost:8080/health | grep 200
  curl -s localhost:8080 | grep 'google.com'
  curl -s localhost:8080/all | grep 'google.com'
  curl -s localhost:8080/days | grep 'google.com'
  curl -s localhost:8080/errors | grep 'nonexisting.host'
}

get_redis_keys () {
  docker compose -f docker-compose-test.yml exec -T redis redis-cli --scan
}

remove_all_containers

cp tests/hosts_mini.lst checker/hosts.lst
build_images "checker" "dashboard"
up_containers "redis" "checker"
sleep 5
list_all_containers
logs_containers "redis" "checker"
get_redis_keys
up_containers "dashboard"
sleep 2
list_all_containers
logs_containers "dashboard"
test_dashboard

docker cp tests/hosts_medium.lst ssl-checker-dashboard-checker-1:/home/app/hosts.lst
sleep 20
list_all_containers
logs_containers "redis" "checker"
get_redis_keys
test_dashboard

docker cp tests/hosts_large.lst ssl-checker-dashboard-checker-1:/home/app/hosts.lst
sleep 30
list_all_containers
logs_containers "redis" "checker"
get_redis_keys
sleep 10
list_all_containers
test_dashboard
remove_all_containers

# git checkout -- checker/hosts.lst
# cp tests/hosts_mini.lst checker/hosts.lst
cp tests/hosts_large.lst checker/hosts.lst
