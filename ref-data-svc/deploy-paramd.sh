# this is differs from the dos approach as running on a mac we need to use the docker buildx feature to build for amd64 rather than arm64
# docker build -t event-data-svc:latest .  # this is for a local build
# parameter $1 is the username $2 is the token/password
echo "deploying for  $1"
docker login -u ociobenablement/identitycloudservice/$1 -p $2  iad.ocir.io
docker buildx build --platform linux/amd64 --push -t iad.ocir.io/ociobenablement/ref-data-svc:latest .
#docker logout iad.ocir.io/ociobenablement/
kubectl apply -f ./deployment.yaml
kubectl apply -f ./ref-data-svc.yaml