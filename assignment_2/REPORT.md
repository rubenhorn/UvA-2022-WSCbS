---
geometry:
- margin=2.3cm
classoption:
- twocolumn
---


# Assignment 2
## Authors:
* Abdellah Lahnaoui (14120429)
* Adrian Aabech (13215566)
* Ruben Horn (13676091)

## JWT authentication
In this assignment, we implement authentication using JSON Web Tokens (JWT) [1] for the URL shortener from assignment 1.
User accounts are managed by a separate microservice with its own persistent storage.  
For the authentication microservice, we re-use most of the code that was previously written for the URL shortener, since it also consists of a simple HTTP server with a persistent repository. Users credentials are stored by username in a key-value store and hashed using SHA256 to protect them against data leaks. For the sake of simplicity, we do not generate a random salt for each user, and instead only include the username and a global secret value in the generation of the password hash. This offers at least some protection for re-used passwords.  
We have already laid the foundation for multiple user support in the URL shortener by storing the owner along with the destination URL and requiring the 'Authorization' header. While this previously contained the user in plain text and no further checks were made, we now decode it from a JWT using a shared secret between the two servers and HMAC with SHA-256. Alternatively, we could have used an asymmetric algorithm which is harder to compromise, since in that case only compromizing the authentication service would allow the attacker to generate tokens for all users, however this does not change the overall setup. Aside from the field `sub` for the username, the payload also contains a timestamp in `iat` and tokens older than one hour will not be accepted. This is necessary to protect the users in the case that a token is stolen.  
In this setup, the two services are decoupled as much as possible and only rely on a shared algorithm and secret.

## Single entry point
Currently, the application consists of three web servers (authentication, URL shortener, static frontend) all running on different ports. Thus, any service consumer has to explicitly reference the host and port of each individual component. To unify them all behind a single host and port, we implement a naive reverse proxy using Flask [2] that forwards requests to a specific host and port based on the longest matching path prefix. In production, one might typically use a Nginx [3] server for this task.

## Scaling
Vertical scaling can not be applied to deal with short term fluctuation in traffic or global traffic. Thus, multiple instances of an application server are instantiated according to the demand (horizontal scaling). The aforementioned reverse proxy may also serve as a load balancer between these instances. This solution requires the application to be stateless and access the same database. In the case of a URL shortener, which is computationally trivial and only acts as a frontend to the database, this alone is not a suitable solution. Instead, a database cluster has to be created where modifications are propagated from the master node and data is eventually consistent. Such functionality is provided, for example by Apache CouchDB [4].

## Service health status
It may happen that an application server becomes unavailable due to a crash. In this case the administrator can restart the application, however, human intervention requires constant monitoring and is generally not very responsive. Alternatively, an orchestration tool (like the Kubernetes controller [5]) can use liveness probes (HTTP status routes) to periodically query the status of an instance. If the probe fails, a new instance can automatically be created.
The application server (or a sidecar) should provide a side-effect free HTTP handler that returns the current status of the service, e.g. 'starting', 'running', 'stopping', 'error state'.

## Performance
We observe a significant increase in severe response time compared to the previous assignment.
This can be attributed to two things:
1. Our naive reverse proxy is not optimized, and we occur a substantial increase in response time owed to an additional HTTP 1.1 request and invocation of a flask handler per request. Production grade proxy servers are implemented using more efficient technologies and may also cache static content.
2. For convenience, we use a single Python script to spawn and terminate all server processes. We have previously observed that using Python instead of shell scripts to do this comes with a significant performance decrease to the child process. A better solution would be to containerize the server applications and orchestrate them using Kubernetes [6] or Docker Compose [7] for simpler scenarios.
As discussed with our TA, invoking DELETE on "/" has not effect, since this operation is very expensive on the database and not useful to many users. The server will responde with HTTP 404 to communicate that "there is nothing to delete".

\pagebreak
# References
\flushleft
- [1] Internet Engineering Task Force, "JSON Web  
\hspace{0.4cm} Token (JWT)", May 2015, [Online].
\hspace{0.4cm} https://datatracker.ietf.org/doc/html/rfc7519.  
\hspace{0.4cm} [Accessed April 20, 2022]. 
 
- [2] Pallets, Flask Documentation, 2010, [Online].  
\hspace{0.4cm}  https://flask.palletsprojects.com/.  
\hspace{0.4cm} [Accessed April 20, 2022].  

- [3] F5 Networks Inc., Nginx website, [Online].  
\hspace{0.4cm} https://www.nginx.com/.  
\hspace{0.4cm} [Accessed April 20, 2022].  

- [4] The Apache Software Foundation, Apache  
\hspace{0.4cm} CouchDB 2021, [Online].  
\hspace{0.4cm} https://couchdb.apache.org/.  
\hspace{0.4cm} [Accessed April 20, 2022].  

- [5] The Kubernetes Authors, Kubernetes  
\hspace{0.4cm} documentation, 2022, [Online].
\hspace{0.4cm} https://kubernetes.io/docs/concepts/architecture/controller/.  
\hspace{0.4cm} [Accessed April 20, 2022].

- [6] The Kubernetes Authors, Kubernetes website,  
\hspace{0.4cm} 2022, [Online].  
\hspace{0.4cm} https://kubernetes.io/.  
\hspace{0.4cm} [Accessed April 20, 2022].

- [7] Docker Inc., Docker Documentation, [Online].  
\hspace{0.4cm} https://docs.docker.com/compose/.  
\hspace{0.4cm} [Accessed April 20, 2022].
