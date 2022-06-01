// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

import { loadSchemaSync } from '@graphql-tools/load';
import EventsInternalAPI from './EventsInternalAPI.js';
import { ApolloServer } from 'apollo-server';
import { GraphQLFileLoader } from '@graphql-tools/graphql-file-loader';
import { resolvers } from './resolvers.js';
import ProviderInternalAPI from './ProvideInternalAPI.js';

// load from a single schema file
const schema = loadSchemaSync('./schema.graphql', {loaders: [new GraphQLFileLoader()]});

const server = new ApolloServer({
  schema,
  resolvers,
  dataSources: () => {
    return { eventsAPI: new eventsInternalAPI(), providerInternalAPI: new ProviderInternalAPI() }
  }});


// The `listen` method launches a web server.
server.listen({ port: 80,}).then(({ url }) => {
  console.log(`🚀  Server ready at ${url}`);
});