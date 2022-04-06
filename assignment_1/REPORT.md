---
title:  Assignment 1
author: Abdellah Lahnaoui, Adrian Aabech, Ruben Horn
geometry: margin=3cm
classoption:
- twocolumn
---

# URL shortener
In this assignment, we implement a URL shortener using Python.
The final application provides an HTTP Application Programming Interface (API) which allows users to map short, random URLs to arbitrary URLs. The short URLs are randomly generated using a shortened Universal Unique Identifier (UUID)^[https://tools.ietf.org/html/rfc4122.html, https://docs.python.org/3/library/uuid.html] to avoid collisions and mitigate enumeration attacks.
The protocol of these URLs must be either HTTP or HTTPS and they are validated by an external Python package^[https://validators.readthedocs.io/en/latest/#module-validators.url].
This implementation does not focus on high performance and does not use advanced features such as pagination.

## Architecture
The application constitutes a simple Create/Read/Update/Delete (CRUD) service.
Thus, we split it into two modules: handlers and repository.

### Handlers
The handlers are implemented using the Flask HTTP framework^[https://flask.palletsprojects.com/] according to the API specification.
The response format adheres to JSend^[https://github.com/omniti-labs/jsend], which is a simple specification to ensure consistent API response formats.

### Repository
We implement two repositories that can be used with the application: ephemeral and persistent.
A concrete repository is selected using a policy pattern at runtime based on the configuration of the application to avoid tight coupling to the handlers.
Since the application is a simple CRUD service that maps short URLs to some destination URLs, the operations of the repository are trivial.
We use a key-value database to store this mapping.
Accessing the destination URL by the short URL can be done very efficiently, depending on the underlying data structure.
The same holds for inserting, updating, or removing values.
These three operations are expected to be the most common in our application.
Selecting one or more keys based on some criteria on the key or value however is a much more expensive operation, since we need to iterate over and test all pairs in the database.
This could be mitigated by using a more advanced database such as DynamoDB^[https://aws.amazon.com/dynamodb/], which allows to efficiently select records using a range key in addition to the primary key.
Our application only uses this inefficient access pattern for listing all stored URLs, which is not a frequent operation.

#### Ephemeral
The ephemeral repository stores all data in a Python dictionary in memory. Data is not persistet accross application restarts.

#### Persistent
The persistent repository stores all data in a flat-file database using shelve^[https://docs.python.org/3/library/shelve.html]. This database is opened at the first access and only closed when the program terminates. After every write-operation, the database is synchronized and the changes are written back to the filesystem.

## Support for multiple users
Only the creator of a shortened URL should be able to modify or remove it.
Thus, we also store the user in the value tuple alongside the destination URL.
Any write operation performs a very simple authorization check by comparing the stored user to the current one.
The current user is determined by the `Authorization` header in the HTTP request.
In our naive implementation, this value represents the username and does not provide any security.
Using JSON Web Tokens (JWT)^[https://datatracker.ietf.org/doc/html/rfc7519] the identity of the user could be verified by the application without transmitting user credentials.
Alternatively, this header may be set by a proxy that sits between the user and the application such as AWS ApiGateway^[https://aws.amazon.com/api-gateway/].

Other URL shorteners also support multiple users:

 * **TinyURL** is a prominent commercial service that identifies anonymous users based on a token that is stored in the browser of the user and also offers user accounts with login credentials.^[http://tinyurl.com]
 * **Shlink** allows the creation and limiting of API keys to modify short URLs.^[https://shlink.io/documentation/api-docs/api-key-roles/]
 * **YOURLS** Protects access to generating shortened links using hardcoded credentials, however, any user can modify them.^[https://github.com/YOURLS/YOURLS/wiki/Username-Passwords]
 * **Kutt, Pckd, Polr** use credentials to limit users to only modify their own short URLs.^[https://kutt.it/, https://github.com/Just-Moh-it/Pckd, https://polrproject.org/]

## Testing
### Test Driven Development (TDD)
The application is developed using TDD in a top-down fashion using pytest^[https://docs.pytest.org/].
We first define the behavior of the application by writing unit tests for each route and HTTP verb.
Then we proceed to implement the corresponding handlers.
The same process is applied to the development of the repository and utility functions.
We test both the ephemeral and persistent repositories, however, the API tests only use the ephemeral repository, which simplifies the tear-down of the tests for them.

### Demo frontend
To carry out manual tests and demonstrate the final product, we provide a simple HTML frontend written in ReactJS^[https://reactjs.org/] which uses the API that the application exposes.
