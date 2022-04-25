# URL shortener
App, auth and frontend servers running behind a naive reverse proxy.

Individual contributions are tracked in [this table](./CONTRIB.csv).

A comprehensive report can be found [here](./REPORT.pdf).

## Requirements
* Docker

## Build containers
Build a container using `docker build -f .\Dockerfiles\<NAME>.Dockerfile -t group6/<NAME> .`.

## Start containers
1. Create a network `docker network create <NET>`.
2. Start database with `docker run --network=<NET> --name=db -e ARANGO_ROOT_PASSWORD=dbPass arangodb`.
3. Run containers `docker run --network=<NET> --name=<NAME> group6/<NAME>`.
4. Run the reverse proxy `docker run --network=<NET> -p 80:80 group6/reverse-proxy`.

## Run servers
Start app on http://localhost/gui/ with `docker compose up --build`

