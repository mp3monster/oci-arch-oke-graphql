// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
// useful link https://www.apollographql.com/tutorials/lift-off-part2/the-shape-of-a-resolver

export const resolvers = {
  Query: {
    event: async (_parent, { id }, { dataSources }, _info)  => {
      console.log("resolvers - Query event id");
      // console.log(parent);
      // console.log(args);
      // console.log(context);
      // console.log(info);
      let apiCall = await dataSources.eventsInternalAPI.getEvent(id);
      console.log(apiCall);
      return apiCall;
      // return {};
    },

    // if there are issues with the resolvers use this to test server config is ok
    help() {
      return "help me";
    },

    latestEvent: async (_parent, _args, { dataSources }, _info) => {
      console.log("resolvers - get latest event");
      return dataSources.eventsInternalAPI.getLatestEvent();
    },

    events: async (_parent, { tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains }, { dataSources }, _info) => {
      console.log( "Query events - tsunami=%s, alert=%s, status=%s, eventType=%s, minTime=%s, maxTime=%s, minMag=%s, maxMag=%s, nameContains=%s", tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains);
      return dataSources.eventsInternalAPI.getEvents(tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains);
    },

    provider: async (_parent, { id }, { dataSources }, _info) => {
      console.log("resolvers - get provider %s", id);
      return dataSources.providerInternalAPI.getProvider(id);
    },

    providers: async (_parent, _args, { dataSources }, _info) => {
      console.log("resolvers get providers");
      return dataSources.providerInternalAPI.getProviders();
    }   
},
  
Mutation: {
  changeEvent: async (_parent, { event }, { dataSources }, _info) => {
    console.log("mutator Change event to %s", event);
    return dataSources.eventsInternalAPI.changeEvent(event);
  },
    deleteEvent: async (_parent, { id }, { dataSources }, _info) => {
    console.log("mutator Change event to %s", id);
    return dataSources.eventsInternalAPI.deleteEvent(id);
  },
  deleteProvider: async (_parent, { code }, { dataSources }, _info) => {
      console.log("mutator remove provider %s", code);
      return dataSources.providerInternalAPI.deleteProvider(code);
    }
  },
};

