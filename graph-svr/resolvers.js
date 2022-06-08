// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
// useful link https://www.apollographql.com/tutorials/lift-off-part2/the-shape-of-a-resolver

// if you don't want the service writing any logs - set this  to false
const log = true;


export const resolvers = {
  Query: {
    event: async (_parent, { id }, { dataSources }, _info)  => {
      if (log) {
        console.log("resolvers - Query event id");
        //console.log(parent); // to use these additional log lines need to change params by removing prefix _
        //console.log(args);
        //console.log(context);
        //console.log(info);
      }
      let responseValue = await dataSources.eventsInternalAPI.getEvent(id);
      if (log) { console.log(`resolved event as: ${responseValue}`); }
      return responseValue;
    },

    // if there are issues with the resolvers use this to test server config is ok
    help() {
      return "help me";
    },

    latestEvent: async (_parent, _args, { dataSources }, _info) => {
      if (log) { console.log("resolvers - get latest event"); }
      let responseValue = await dataSources.eventsInternalAPI.getLatestEvent();
      if (log) { console.log(`Resolver response for latest event:\n ${responseValue}`); }
      return responseValue;
    },

    events: async (_parent, { tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains }, { dataSources }, _info) => {
      if (log) { console.log("Query events - tsunami=%s, alert=%s, status=%s, eventType=%s, minTime=%s, maxTime=%s, minMag=%s, maxMag=%s, nameContains=%s", tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains); }
      let responseValue = dataSources.eventsInternalAPI.getEvents(tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains);
      if (log) { console.log(`Get events returned: \n ${responseValue}`); }
      return responseValue;
    },

    provider: async (_parent, { code }, { dataSources }, _info) => {
      if (log) { console.log("resolvers - get provider %s", code); }
      let responseValue = await dataSources.providerInternalAPI.getProvider(code);
      if (log) { console.log(`Get provider returned: \n ${responseValue}`); }

      return responseValue;
    },

    providers: async (_parent, _args, { dataSources }, _info) => {
      if (log) { console.log("resolvers get providers"); }
      let responseValue = await dataSources.providerInternalAPI.getProviders();
      if (log) { console.log(`Get providers returned: \n ${responseValue}`); }

      return responseValue;      
    }   
},
  
Mutation: {
  changeEvent: async (_parent, { event }, { dataSources }, _info) => {
    if (log) { console.log("mutator Change event to %s", event); }
    return dataSources.eventsInternalAPI.changeEvent(event);
  },
    deleteEvent: async (_parent, { id }, { dataSources }, _info) => {
    if (log) { console.log("mutator Change event to %s", id); }
    return dataSources.eventsInternalAPI.deleteEvent(id);
  },
  deleteProvider: async (_parent, { code }, { dataSources }, _info) => {
    if (log) { console.log("mutator remove provider %s", code); }
      return dataSources.providerInternalAPI.deleteProvider(code);
    }
  },
};

