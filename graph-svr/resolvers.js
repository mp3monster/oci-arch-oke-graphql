// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

export const resolvers = {
  Query: {
    event: async (_, { id }, { dataSources }) => {
      return await dataSources.eventsInternalAPI.getEvent(id);
    },
    events: async (_, { tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains }, { dataSources }) => {
        return await dataSources.eventsInternalAPI.getEvents(tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains);
    },
    provider: async (_, { id }, { dataSources }) => {
        return await dataSources.providerInternalAPI.getProvider(id);
    },
    providers: async (_, __, { dataSources }) => {
        return await dataSources.providerInternalAPI.getProviders();
    },   
},
  
Mutation: {
  changeEvent: async (_, { event }, { dataSources }) => {
    return await dataSources.eventsInternalAPI.changeEvent(event);
  },
  removeProvider: async (_, { code }, { dataSources }) => {
      return await dataSources.eventsInternalAPI.deleteProvider(code);
    },
  },
};