# Copyright(c) 2022, Oracle and / or its affiliates.
# All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
#
# useful resources
# https://flask.palletsprojects.com/en/2.1.x/

from flask import Flask, request, Response
import configparser
import json
import os

app = Flask(__name__)


def getconfig():
    config = configparser.RawConfigParser()
    config.read('ref-data-svc.cfg')

    return config


def loaddata(config):

    # Opening JSON file
    filehandle = open(config.get('providers', 'file'))
    refdata = json.load(filehandle)
    filehandle.close()

    return refdata


def prep_provider_alternates(providerdata):
    updatedprovider = providerdata.copy()

    print("provider count=" + str(len(providerdata)))
    for provider in providerdata:
        if 'aka' in provider:
            aka_list = provider['aka']
            for aka in aka_list:
                newprovider = provider
                newprovider['code'] = aka
                updatedprovider.append(newprovider)
                print(newprovider)

    print("UPDATED provider count=" + str(len(updatedprovider)))

    return updatedprovider


def get_provider_by_id(id):
    print("looking for " + id)
    for provider in providerdata:
        print(provider)
        code = provider.get('code')
        if (code.lower() == id.lower()):
            return provider
    return None


def get_provider_by_name(name):
    print("looking for " + name)
    for providerid in providerdata:
        if (providerdata[providerid].lower().contains(name.lower())):
            return providerdata[providerid]
    return None


@ app.route('/provider', methods=['GET'])
def get_provider():
    refelement = None
    resultstr = ""

    if (request.args != None) and (len(request.args) > 0):
        for arg in request.args:
            if (arg == "id"):
                refelement = get_provider_by_id(request.args['id'])
            elif (arg == "name"):
                refelement = get_provider_by_name(request.args['name'])
    else:
        refelement = providerdata

    if (refelement != None):
        resultstr = json.dumps(refelement, indent=2, sort_keys=False)

    return resultstr


@ app.route('/provider', methods=['DELETE'])
def delete_provider():
    response = Response(status=410)
    if (request.args != None) and (len(request.args) > 0)):
        id=request.args['id'];
        if (id != None):
            for providerId in providerdata:
                provider=providerdata[providerId]
                if (provider['code'].lower() == id):
                    providerdata.remove(providerId)
                    response=Response(status = 200)
                elif 'aka' in provider:
                    aka_list=provider['aka']
                    if id in aka_list:
                        aka_list.remove(id)


    return response

@ app.route('/test/')
def test():
    return "hello world"


@ app.route('/health')
def health():
    status=dict()
    status['provider-data']=len(providerdata)
    status['config']=config
    return json.dumps(status, indent = 2, sort_keys = False)


config=getconfig()
os.environ['host']=config.get('server', 'host')
os.environ['port']=config.get('server', 'port')

providerdata=loaddata(config)
providerdata=prep_provider_alternates(providerdata)

if __name__ == '__main__':
    app.run(debug = config.getint('server', 'debug'),
            port = config.getint('server', 'port'),
            host = config.get('server', 'host'))
