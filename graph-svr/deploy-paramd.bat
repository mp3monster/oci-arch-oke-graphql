rem # Copyright(c) 2022, Oracle and / or its affiliates.
rem # All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

rem build the docker image and set the tag
# %1 is the username 
# %2 is the token/password
# %3 is the Tenancy name
# %4 is the OCI Region in short form e.g. iad

set name=graphql-svr-svc

echo deploying %name% for %1
echo 

docker build -t %name% .
docker tag %name%:latest %4.ocir.io/%3/%name%:latest

rem acces OCIR and upload the container
echo logging in %3/identitycloudservice/%1 -p %2  %4.ocir.io
docker login -u %3/identitycloudservice/%1 -p %2  %4.ocir.io

echo pushing %4.ocir.io/%3/%name%:latest
docker push %4.ocir.io/%3/%name%:latest

rem deploy the container and then the service wrapper
kubectl apply -f ./deployment.yaml
rem kubectl apply -f ./%name%.yaml

kubectl delete pod -l app=graphql-svr-pod