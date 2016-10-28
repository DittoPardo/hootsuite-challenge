# hootsuite-challenge
A simple project to experiment with flask, mongodb, docker, py.test, python3, reddit api (praw), reactJs, mobx, webpack,
babel, jest

## Requirements

This was tested on a linux machine. If your are using Mac a configured docker-machine will probably be also required.

docker >= 1.10 (1.12 was used)
docker-compose >= 1.6 (1.8 was used)
 
This project uses (official) images stored on docker hub

## Run

`docker-compose up [-d]`

containers are named 
 - hsc_web: the flask web service
 - hsc_webpack: the webpack dev server for live refresh. Also takes care of flask assests. On production buils this
 container compiles js, css, images and manifest.json for flask assets and exits.
 - hsc_mongo: the mongo service
 - hsc_feeder: the script that fetches data from reddit periodically. it is client server based on unix socket. brings up cron too
 - hsc_redis: has no purpose except for a small demo, but it will have a greater role to play

Alternatively one may use the shell scripts for convenience:
 - ./debug.sh [container name], starts the suite but with designated container attached to a tty and stdin; use for interactive debugging
 - ./test.sh [container name], test environment; one can run py.test from that shell 
 - ./shell.sh [containter name], exec an additional bash shell inside container
 - ./log.sh [container name], show 100 lines and future lines from designated container logs
 
 ## hsc_feeder
 
 One can give ondemand commands to hsc_feeder by `./shell.sh hsc_feeder` followed by a call to any of `./*_command.py` clients
 The client run by crontab is logging in /var/log/read-command.log . This is not very dockerish and needs to change.
 The logs are merely for example; timestamps and other important logging behaviours were left aside...
 
 ## Usage
 
 Upon suite start the hsc_feeder will start grabbing reddits every 15 min.
 The fetching involves only new posts (submission and comments) and is not designed to collect them all (the newest 25 sumbmissions)
 One can configure what subreddits are fetched from feeder-service/settings.py, SUBREDDITS list.
 
 the hsc_web container runs a web service, a flask in debug mode for now, exposed on your host on port 80
 one may connect through browser, on localhost and access the following endpoint:
 `http://localhost/items?subreddit=<x>&from=<ti>&to=<tf>&keyword=<word>`
 for example:
 `http://localhost/items?subreddit=python&from=1475900000&to=1475999999&keyword=simple%20weird`
 will search the so far indexed reddits for submissions and comments, under subreddit 'python', between timestamps from and to,
 containing, case insensitive, any of the words 'simple' or 'weird' in any of the submission title or comment text.
 
 
 ## Notes
 If anything changes to the requirements.txt files docker will not be aware of it since nothing changed to Dockerfile
 In this case manually rebuild the image.
 `docker build -t hootsuite_[web|feeder] -f docker/[web|feeder-service]/Dockerfile .`
 
 docker/.envs/common.env holds environment variables aplicable to all containers
 docker/web/.envs/*.env, for instance holds specific env vars
 
 ## Todo
 - Better test coverage, e2e tests
 - Add test framework to front end
 - mongos and shards
 
 ## End
 Hope you found this mini project useful and pleasant.
 Feel free to suggest changes if you see a more elegant or straight forward way to do things.
 Thanks!
 
 
 
