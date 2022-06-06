# Copyright(c) 2022, Oracle and / or its affiliates.
# All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
#
# useful resources
# https://flask.palletsprojects.com/en/2.1.x/

from flask import Flask, request, Response
import configparser
import json
import os
import logging
import sys


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

    logger.debug("provider count=" + str(len(providerdata)))
    for provider in providerdata:
        if 'aka' in provider:
            aka_list = provider['aka']
            for aka in aka_list:
                newprovider = provider
                newprovider['code'] = aka
                updatedprovider.append(newprovider)
                logger.debug(newprovider)

    logger.debug("UPDATED provider count=" + str(len(updatedprovider)))

    return updatedprovider


def get_provider_by_id(id):
    logger.debug("looking for " + id)
    for provider in providerdata:
        logger.debug(provider)
        code = provider.get('code')
        if (code.lower() == id.lower()):
            return provider
    return None


def get_provider_by_name(name):
    logger.debug("looking for " + name)
    for providerid in providerdata:
        if (providerdata[providerid].lower().contains(name.lower())):
            return providerdata[providerid]
    return None


@ app.route('/provider', methods=['GET'], strict_slashes=False)
def get_provider():
    ref_element = None
    resultstr = ""

    if (request.args != None) and (len(request.args) > 0):
        for arg in request.args:
            if (arg == "id"):
                ref_element = get_provider_by_id(request.args['id'])
            elif (arg == "name"):
                ref_element = get_provider_by_name(request.args['name'])
    else:
        ref_element = providerdata

    if (ref_element != None):
        resultstr = json.dumps(ref_element, indent=2, sort_keys=False)

    return resultstr


@ app.route('/provider', methods=['DELETE'], strict_slashes=False)
def delete_provider():
    response = Response(status=410)
    request_id = None
    if (request.args != None) and (len(request.args) > 0):
        request_id = request.args['id']

    if (request_id != None):
        for provider_id in providerdata:
            provider = providerdata[provider_id]
            if (provider['code'].lower() == id):
                providerdata.remove(provider_id)
                response = Response(status=200)
            elif 'aka' in provider:
                aka_list = provider['aka']
                if id in aka_list:
                    aka_list.remove(id)
    return response


@ app.route('/test/',  methods=['GET'], strict_slashes=False)
def test():
    return "confirming, test ok"


@ app.route('/health/',  methods=['GET'], strict_slashes=False)
def health():
    status = dict()
    status['provider-data'] = len(providerdata)
    status['config'] = config

    json = json.dumps(status, indent=2, sort_keys=False)
    logger.debug(json)
    return json


@app.errorhandler(404)
def page_not_found(error):
    logger.warning("Error handler caught request : %s", str(request.data))
    return 'URL not found', 404


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

config = getconfig()
os.environ['host'] = config.get('server', 'host')
os.environ['port'] = config.get('server', 'port')

logger.debug("debug ==>" + str(config.get('server', 'debug')))
logger.debug("port ==>" + str(config.getint('server', 'port')))
logger.debug("host ==>" + config.get('server', 'host'))

providerdata = loaddata(config)
providerdata = prep_provider_alternates(providerdata)

if __name__ == '__main__':
    app.run(debug=config.getint('server', 'debug'),
            port=config.getint('server', 'port'),
            host=config.get('server', 'host'))
