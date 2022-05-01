# URL shortener
Database app, auth and frontend servers running behind a reverse proxy.

Individual contributions are tracked in [this table](./CONTRIB.csv).

A comprehensive report can be found [here](./REPORT.pdf).

## Requirements
* Docker

## Build containers
Build a container using `./Dockerfiles/build-all`.

## Run containers manually
1. Create a network using `docker network create <NET>`.
2. Start the database with `docker run --network=<NET> --name=db -e ARANGO_ROOT_PASSWORD=dbPass arangodb`.
3. Run containers using `docker run --network=<NET> --name=<NAME> luoabd/group6-<NAME>`.  
(You may need to provide additional environment variables as done using [Docker Compose](compose.yaml).)
4. Run the reverse proxy with `docker run --network=<NET> -p 80:80 luoabd/group6-reverse-proxy`.

## Deploy app using Docker Compose
Start the complete app on http://localhost/gui/ with `docker compose up --build`.

## Deploy app to Kubernetes cluster
1. Build images as described above.
2. Deploy the app to a Kubernetes cluster with `./K8s/deployment up`.
3. Run the external load balancer with `docker run -d --mount src="$(pwd)/load-balancer",target=/etc/nginx/conf.d,type=bind -p 80:80 --name load-balancer --restart unless-stopped nginx`.
