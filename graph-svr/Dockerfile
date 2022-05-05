# Copyright(c) 2022, Oracle and / or its affiliates.
# All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
FROM oraclelinux:8-slim
RUN microdnf install oracle-instantclient-release-el8 oraclelinux-developer-release-el8
RUN EXPORT NODE_PATH=$(npm root -g)
ADD *.py *.json *.cfg *.js *.graphql
RUN npm install
COPY . /app
WORKDIR /app
EXPOSE 4000
CMD ["npm", "start index.js"]
HEALTHCHECK --start-period=5s --timeout=4s CMD curl -f localhost:4000/ || exit 1