# TITLE

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_test)](https://sonarcloud.io/dashboard?id=oracle-devrel_test)

## THIS IS A NEW, BLANK REPO THAT IS NOT READY FOR USE YET.  PLEASE CHECK BACK SOON!

## Introduction
MISSING

## Getting Started
MISSING

### Prerequisites
This Reference Architecture is not yet equipped with one click deploy. However the deployment process can be accelerated by using the following automated deployment - https://docs.oracle.com/en/solutions/deploy-oke-with-atp-in-oci/index.html but during the configuration value setting in the Resource Manager you can omit the deployment of the ATP.

Once done the infrastructure will also need Oracle Container Registries (OCIR) created for:
- graphql-svr
- event-data-svc
- ref-data-svc
  

Creation of a Virtual Service Gateway so that OKE can see OCIR.
2 user auth keys. 1 to be put into a secret as described by XXX
## Notes/Issues
MISSING

## URLs

* [OCIR Overview](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryoverview.htm)
* [OKE docs](https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm)
* [Deploying from OCIR into OKE](https://www.oracle.com/webfolder/technetwork/tutorials/obe/oci/oke-and-registry/index.html) - setup steps

## Contributing

This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

## License
Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK. 