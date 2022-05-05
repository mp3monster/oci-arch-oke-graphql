// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

import { RESTDataSource } from 'apollo-datasource-rest';
import fs from 'fs';

export default class ProviderInternalAPI extends RESTDataSource {
  constructor() {
    super();
    let config = JSON.parse(fs.readFileSync('./config.json'));
    this.baseURL = config['ref-data-svc-base'];
  }

  // GET
  async getProvider(code) {
    request.params.set('id', code);
    return this.get(`provider`);
  }

  // GET
  async getProviders() {
    return this.get(`providers`);
  }

  // DELETE
  async deleteProvider(id) {
    request.params.set('id', id);
    return this.delete();
  }
}