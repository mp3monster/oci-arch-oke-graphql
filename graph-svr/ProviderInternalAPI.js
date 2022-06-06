// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

import { RESTDataSource } from 'apollo-datasource-rest';
import fs from 'fs';

export default class ProviderInternalAPI extends RESTDataSource {
  constructor() {
    super();
    let config = JSON.parse(fs.readFileSync('./config.json'));
    this.baseURL = 'http://' + config['ref-data-svc-base'];
    console.log("Ref REST Data Source:"+this.baseURL);
  }

  // GET
  async getProvider(code) {
    console.log("getProvider (%s) directing to %s",code,this.baseURL);
    request.params.set('id', code);
    return this.get(`provider`);
  }

  // GET
  async getProviders() {
    console.log("getProviders directing to %s",this.baseURL);
    return this.get(`providers`);
  }

  // DELETE
  async deleteProvider(id) {
        console.log("deleteProvider directing to %s",id, this.baseURL);
    request.params.set('id', id);
    return this.delete();
  }
}