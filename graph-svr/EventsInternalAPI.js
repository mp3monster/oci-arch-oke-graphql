// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

import { RESTDataSource } from 'apollo-datasource-rest';
import fs from 'fs';

export default class EventsInternalAPI extends RESTDataSource {
  constructor() {
    super();
    let config = JSON.parse(fs.readFileSync('./config.json'));
    this.baseURL = config['event-svc-base'];
  }

  // GET
  async getEvent(id) {
    request.params.set('id', id);
    return this.get(`event`);
  }

  // GET
  async getEvents(tsunami, alert, status, eventType, minTime, maxTime, minMag, maxMag, nameContains) {
    if (tsunami != null) { request.params.set('tsunami', tsunami); }
    if (alert != null) { request.params.set('alert', alert); }
    if (status != null) { request.params.set('status', status); }
    if (eventType != null) { request.params.set('eventType', eventType); }
    if (minTime != null) { request.params.set('minTime', minTime); }
    if (maxTime != null) { request.params.set('maxTime', maxTime); }
    if (minMag != null) { request.params.set('minMag', minMag); }
    if (maxMag != null) { request.params.set('maxMag', maxMag); }
    if (nameContains != null) { request.params.set('nameContains', nameContains); }
 
    return this.get(`events`);
  }

  // POST
  async changeEvent(event) {
    return this.post(
      `event`, // path
      event // request body
    );
  }

  // PUT
  async newEvent(event) {
    return this.put(
      `event`, // path
      event // request body
    );
  }

  // DELETE
  async deleteEvent(Id) {
    request.params.set('id', id);
    return this.delete(`event`);    
}