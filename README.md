# TITLE

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_test)](https://sonarcloud.io/dashboard?id=oracle-devrel_test)

## THIS IS A NEW, BLANK REPO THAT IS NOT READY FOR USE YET.  PLEASE CHECK BACK SOON!

## Introduction
This Reference Architecture has been implemented to achieve the following:

- Illustrate  how GraphQL can be implemented to be highly scalable (many example implementations put the new logic within the GraphQL Server here we adopt a scalable approach)
- Deployment from OCIR into OKE
- Composability of architectural solutions by deploying this RA on top of a more basic RA.
- Illustrate how we can use OCI API Gateway to implement security in front of a Kubernetes cluster.

The solution deploys three containers that perform the following actions:

- Hosts an instance of the Apollo GraphQL server implemented with Node JS
- A Python 3 service using Flask that servers data for Earthquake events
- A Python 3 service that provides additional data about different Earthquake monitoring stations.

The implementation of these services has taken inspiration from the US Geographical Survey (links provided below). The two Python services take their data from a JSON file held within the service and the files are loaded and processed into memory. As a result, restarting the services will reset the data. 

We have taken this approach to keep the setup simple - so we don't get distracted by the additional effort of configuring database connections.

In the reference diagram, we illustrate the static content being delivered separately. This would be the recommended approach to deploying the static HTML and JavaScript that will drive the presentation view and perform the API calls to retrieve the web application data. This implementation has not implemented this functionality as it doesn't further the goals described in the introduction.

## Getting Started

To be able to experiment with the solution you will need to set up the development tooling described.

### Prerequisites

#### Developer tooling

- Node JS & Python 3 along with their tools
- Docker

The following tooling needs to be installed:

- Kubernetes CLI (kubectl)
- OCI CLI

We would also recommend using an IDE such as Visual Studio Code.

#### OCI Setup

OCI needs to be configured with the services illustrated in the architecture diagram - available at XXX. In the deployment we would recommend the following items be included:

- Public IP for OKE so that the resolver services can be exercised directly (simplify testing) - this can be disabled in the future.
- The API Gateway is deployed in the public subnet. The network traffic will require the routing to be permissible from the gateway.
- Configuration of the Gateways as described [here](./docs/api-config.md).
- The microservices need to be deployed. The details to do that are [here](./docs/k8s-configuration).

## Notes/Issues

To deploy from the relevant OCIR registry we need to set up a secret and incorporate the secret into our deployment commands. This is illustrated at [oracle.com/webfolder/technetwork/tutorials/obe/oci/oke-and-registry/index.html](https://kubernetes.io/docs/tasks/tools/).

More information on how the Kubernetes configuration for the example can be found [here](./docs/k8s-configuration).

#### Potential enhancements

Improvements that could be applied to this solution:

- incorporate the use of Helm charts to deploy the services
- Provide Open API specifications for the API definitions
- Extend the example to use OCI Certificates
- Terraform optional control to enable the Kubernetes Dashboard deployment

## URLs

* [OCIR Overview](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryoverview.htm)
* [OKE docs](https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm)
* [OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm)
* [Deploying from OCIR into OKE](https://www.oracle.com/webfolder/technetwork/tutorials/obe/oci/oke-and-registry/index.html) - setup steps
* [Installing Kubectl](https://kubernetes.io/docs/tasks/tools/)
* [API Gateway Deployment Parameter Description](https://docs.oracle.com/en-us/iaas/Content/APIGateway/Tasks/apigatewaycreatingdeployment.htm)

#### Learn more about USGS data

Background information on Earthquake monitoring and measurement.

- [USGS Data explanations](https://earthquake.usgs.gov/data/comcat/index.php)
- [Rules for using USGS Data](https://www.usgs.gov/science/faqs/data-tools-and-technology)
- [Example USGS Earthquake Data set](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson)
- [GeoJSON](https://geojson.org/) Definition - standard for describing Geographical structures.
- [Contributors to USGS monitoring data](https://earthquake.usgs.gov/data/comcat/contributor/) (the basis of our Reference data service)

## Contributing

This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

## License
Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK. 