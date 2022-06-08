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


def get_provider_by(id, element):
    logger.debug("looking for %s in element %s", id, element)
    identified_provider = None
    lower_id = id.lower()

    for provider in providerdata:
        value = provider.get(element)
        if (value.lower() == lower_id):
            identified_provider = provider
            break

    return identified_provider


@ app.route('/provider', methods=['GET'], strict_slashes=False)
def get_provider():
    ref_element = None
    responsestr = None
    response_code = 404

    if (request.args != None) and (len(request.args) > 0):
        for arg in request.args:
            if (arg == "code"):
                ref_element = get_provider_by(request.args['code'], 'code')
            elif (arg == "name"):
                ref_element = get_provider_by(
                    request.args['name'], 'name')

    if (ref_element != None):
        responsestr = json.dumps(ref_element, indent=2, sort_keys=False)
        response_code = 200

    response = Response(response=responsestr,
                        status=response_code,
                        content_type="application/json")
    return response


@ app.route('/provider', methods=['DELETE'], strict_slashes=False)
def delete_provider():
    response_code = 410

    request_id = None
    if (request.args != None) and (len(request.args) > 0):
        request_id = request.args['id']

    if (request_id != None):
        for provider_id in providerdata:
            provider = providerdata[provider_id]
            if (provider['code'].lower() == id):
                providerdata.remove(provider_id)
                response_code = 200
            elif 'aka' in provider:
                aka_list = provider['aka']
                if id in aka_list:
                    aka_list.remove(id)

    response = Response(response=None,
                        status=response_code,
                        content_type="application/json")
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

logger.debug("========== Preparing ==========")

config = getconfig()
os.environ['host'] = config.get('server', 'host')
os.environ['port'] = config.get('server', 'port')

logger.debug("debug ==>" + str(config.get('server', 'debug')))
logger.debug("port ==>" + str(config.getint('server', 'port')))
logger.debug("host ==>" + config.get('server', 'host'))

providerdata = loaddata(config)
providerdata = prep_provider_alternates(providerdata)

logger.debug("========== ready ==========")

if __name__ == '__main__':
    app.run(debug=config.getint('server', 'debug'),
            port=config.getint('server', 'port'),
            host=config.get('server', 'host'))
