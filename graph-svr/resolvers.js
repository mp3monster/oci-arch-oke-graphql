// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

export const resolvers = {
  Query: {
    event: async (_, { id }, { dataSources }) => {
      console.log("resolvers - Query event id %s", id);
      return await dataSources.eventsInternalAPI.getEvent(id);
    },
    events: async (_, { tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains }, { dataSources }) => {
        console.log("resolvers", "Query events", tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains);
        return await dataSources.eventsInternalAPI.getEvents(tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains);
    },
    provider: async (_, { id }, { dataSources }) => {
        console.log("resolvers - get provider %s", id);
        return await dataSources.providerInternalAPI.getProvider(id);
    },
    providers: async (_, __, { dataSources }) => {
        console.log("resolvers get providers");
        return await dataSources.providerInternalAPI.getProviders();
    },   
},
  
Mutation: {
  changeEvent: async (_, { event }, { dataSources }) => {
    console.log("mutator Change event to %s", event);
    return await dataSources.eventsInternalAPI.changeEvent(event);
  },
  removeProvider: async (_, { code }, { dataSources }) => {
      console.log("mutator remove provider %s", id);
      return await dataSources.eventsInternalAPI.deleteProvider(code);
    },
  },
};