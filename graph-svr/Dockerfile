# Copyright(c) 2022, Oracle and / or its affiliates.
# All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
FROM oraclelinux:8
RUN dnf -y module enable nodejs:16 && \
  dnf -y install nodejs npm && \
  rm -rf /var/cache/dnf
ADD *.json *.cfg *.js *.graphql ./
RUN npm install
COPY . /app
WORKDIR /app
EXPOSE 4000
CMD ["/bin/npm", " start index.js"]
HEALTHCHECK --start-period=5s --timeout=5s CMD curl -f localhost:4000/ || exit 1