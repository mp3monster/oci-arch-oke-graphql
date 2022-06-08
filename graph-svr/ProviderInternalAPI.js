// Copyright(c) 2022, Oracle and / or its affiliates.
// All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl

import { RESTDataSource } from 'apollo-datasource-rest';
import fs from 'fs';

export default class ProviderInternalAPI extends RESTDataSource {
  constructor() {
    super();
    let config = JSON.parse(fs.readFileSync('./config.json'));
    this.baseURL = 'http://' + config['ref-data-svc-base']+'/';
    console.log("Ref REST Data Source:"+this.baseURL);
  }

  // GET
  async getProvider(code) {
    console.log("getProvider (%s) directing to %s",code,this.baseURL);
    return this.get(`provider?code=${code}`);
  }


    // build up the params part of the url prefixing as appropriate
  addParam(params, name, value)
  {
    if (params == '')
    {
      params = params + '?';
    }
    else
    {
      params = `${params}&`;
    }
  
    params = `${params}${name}=${value}`;
    return params;
  }

  // GET
  async getProviders(code, alias, name) {
    console.log("getProviders directing to %s", this.baseURL);
    
    let params = '';
    if (code != null) { params = addParam(params, 'code', code); }
    if (alias != null) { params = addParam(params, 'alias', alias); }
    if (name != null) { params = addParam(params, 'name', name); }
    
    return this.get(`providers${params}`);
  }

  // DELETE
  async deleteProvider(code) {
        console.log("deleteProvider directing to %s",id, this.baseURL);
    return this.delete();
  }
}