# Copyright(c) 2022, Oracle and / or its affiliates.
# All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
FROM oraclelinux:8
WORKDIR /app
EXPOSE 4000
ADD *.json *.cfg *.js *.graphql probe.sh ./
RUN dnf -y module enable nodejs:16 && \
  dnf -y install nodejs npm && \
  rm -rf /var/cache/dnf
RUN npm install
ENTRYPOINT ["/bin/npm", "start"]