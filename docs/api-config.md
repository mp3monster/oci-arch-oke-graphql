## API Gateway Configuration



We want to create several simple Deployments into the API Gate. Each of the following sections describes the API and the deployment parameters

Where URLS are required these need to be URLs of the Kubernetes entry points. These can be set by copying the **Kubernetes API Private Endpoint** the OKE configuration and appending the service name to the end, so you should have something like:

***10.0.0.131:6443***/ref-data-svc

## Test

This will allow us to validate that we can invoke the API Gateway properly and will return a result through the correct path. Once everything is deployed correctly this can be deleted. Within the test group, we will include direct paths to our resolvers for the purposes of testing and changes.



##### Basic Information

| Attribute   | Value |
| ----------- | ----- |
| Name        | Test  |
| Path prefix | /test |
|             |       |

##### API Request policies

| Attribute                                     | Value               |
| --------------------------------------------- | ------------------- |
| Mutual-TLS                                    | -- no values set -- |
| Authentication                                | -- no values set -- |
| CORS                                          | -- no values set -- |
| Rate limiting                                 |                     |
| Rate limiting - Number of requests per second | 1                   |
| Rate limiting - Type of rate limit            | Total               |
| Usage plans                                   | -- no values set -- |

##### API logging policies

| Attribute           | Value       |
| ------------------- | ----------- |
| Execution log level | information |

#### Route 1

| Attribute    | Value                  |
| ------------ | ---------------------- |
| Path         | /test                  |
| Methods      | GET                    |
| Type         | Stock response         |
| Status code  | 200                    |
| Body         | {"test":"response ok"} |
| Header name  | -- no value set--      |
| Header value | -- no value set --     |

#### Route 2

| Attribute                                   | Value                  |
| ------------------------------------------- | ---------------------- |
| Path                                        | /events                |
| Methods                                     | GET, POST, DELETE      |
| Type                                        | HTTP                   |
| URL                                         | xxxx                   |
| Body                                        | {"test":"response ok"} |
| Connection establishment timeout in seconds | -- no value set--      |
| Reading response timeout in seconds         | -- no value set --     |
| Disable SSL verification                    | set                    |

#### Route 3

| Attribute                                   | Value                  |
| ------------------------------------------- | ---------------------- |
| Path                                        | /refdata               |
| Methods                                     | GET, POST, DELETE      |
| Type                                        | HTTP                   |
| URL                                         | xxxx                   |
| Body                                        | {"test":"response ok"} |
| Connection establishment timeout in seconds | -- no value set--      |
| Reading response timeout in seconds         | -- no value set --     |
| Disable SSL verification                    | set                    |



## GraphQL

This endpoint will direct the traffic to our GraphQL server.  We will prefix the path for our implemented services as /svc so our services would be /svc/data



##### Basic Information

| Attribute   | Value          |
| ----------- | -------------- |
| Name        | GraphQL Server |
| Path prefix | /svc           |
|             |                |

##### API Request policies

| Attribute                                             | Value               |
| ----------------------------------------------------- | ------------------- |
| Mutual-TLS                                            | -- no values set -- |
| Authentication                                        | -- no value set --  |
| Header validations                                    |                     |
| Header validations - Add body validation - Required   | Set                 |
| Header validations - Add body validation - Media type | application/json    |
| CORS                                                  | -- no values set -- |
| Rate limiting                                         |                     |
| Rate limiting - Number of requests per second         | 1                   |
| Rate limiting - Type of rate limit                    | Total               |
| Usage plans                                           | -- no values set -- |

##### API logging policies

| Attribute           | Value       |
| ------------------- | ----------- |
| Execution log level | information |

#### Route 1

| Attribute                                   | Value                  |
| ------------------------------------------- | ---------------------- |
| Path                                        | /svc                   |
| Methods                                     | GET, POST, DELETE      |
| Type                                        | HTTP                   |
| URL                                         | xxxx                   |
| Body                                        | {"test":"response ok"} |
| Connection establishment timeout in seconds | -- no value set--      |
| Reading response timeout in seconds         | -- no value set --     |
| Disable SSL verification                    | set                    |

