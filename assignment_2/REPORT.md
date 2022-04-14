---
geometry:
- margin=2.5cm
---


# Assignment 2
## Authors:
* Abdellah Lahnaoui (14120429)
* Adrian Aabech (13215566)
* Ruben Horn (13676091)

## JWT authentication
In this assignment, we implement authentication using JSON Web Tokens (JWT) [1] for the URL shortener from assignment 1.
User accounts are managed by a seperate microservice with its own repository.

For the authentication microservice, we re-use most of the code that was previously written for the URL shortener, since it also consists of a simple HTTP server with a persistent repository. Users credentials are stored by username in a key-value store and hashed using SHA256 to protect them against data leaks. For the sake of simplicity, we do not generate a random salt for each user and instead only include the username and a secret value in the generation of the password hash. This offers at least some protection for re-used passwords.

We have already laid the foundation for multiple user support in the URL shortener by storing the owner along with the destiantion url and requiring the 'Authorization' header. While this previously contained the user in plain text and no further checks were made, we now decode it from a JWT using a shared secret between the two servers and HMAC with SHA-256. Alternatively, we could have used an asymmetric algorithm which is harder to compromize, however this does not change the overall setup. Aside from the field `sub` for the username, the payload also contains a timestamp in `iat` and tokens older than one hour will not be accepted. This is necessary to protect the users in the case that a token is stolen.

## Single entrypoint
Currently the application consists of three web servers (authentication, URL shortener, static frontend) all running on different ports. Thus, any service consumer has to explicitly reference the host and port of each individual component. To unify them all behind a single host and port we implement a naive reverse proxy using Flask [2] that forwards requests to a specific host and port based on the longest matching path prefix. In production, one might typically use an Nginx [3] server for this task.

## Scaling
Vertical scaling can not be applied to deal with short term fluctuation in traffic or global traffic. Thus, multiple instances of an application server are instantiated according to the demand (horizontal scaling). The aforementioned reverse proxy may also serve as a load balancer between these instances. This solution requires the application to be stateless and access the same database. In the case of a URL shortener, which is computationally trivial and only acts as a frontend to the database, this alone is not a suitable solution. Instead, a database cluster has to be created where modifications are propagated from the master node and data is eventually consistent. Such functionality is provided for example by Apache CouchDB [4].

## Service health status
It may happen that an application server becomes unavailable due to a crash. In this case the administrator can restart the application, however, human intervention requires constant monitoring and is generally not very responsive. Alternatively, an orchestration tool (like the Kubernetes controller [5]) can use liveness probes (HTTP status routes) to periodically query the status of an instance. If the probe fails, a new instance can automatically be created.

\pagebreak
# References
\flushleft
[1] https://datatracker.ietf.org/doc/html/rfc7519  
[2] https://flask.palletsprojects.com/  
[3] https://www.nginx.com/  
[4] https://couchdb.apache.org/  
[5] https://kubernetes.io/docs/concepts/architecture/controller/
