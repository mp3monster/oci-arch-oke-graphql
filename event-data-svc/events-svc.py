
# Copyright(c) 2022, Oracle and / or its affiliates.
# All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
#
# useful resources
# https://flask.palletsprojects.com/en/2.1.x/
#


from importlib.metadata import metadata
import json
import os
from flask import Flask, request, Response
import configparser
from decimal import *
import logging
import sys


app = Flask(__name__)


def getconfig():
    config = configparser.RawConfigParser()
    config.read('event-svc.cfg')

    return config


def loaddata(config):

    # Opening JSON file
    filehandle = open(config.get('data', 'file'))
    logger.info("using data set %s", filehandle)
    eventdata = json.load(filehandle)
    filehandle.close()

    return eventdata

# separate the metadata record from the events


def extractmetadata(eventdata):
    for event in eventdata:
        if (event["type"] == "FeatureCollection"):
            return event

    logger.info("No metadata found")
    return None


def cleansedata(eventdata):
    messages = "cleansing data -\n"
    cleandata = []

    for event in eventdata:
        if (event["type"] == "FeatureCollection"):
            messages += "Located meta data entry\n"
        elif (event["type"] == "Feature"):
            properties = event["properties"]
            properties["id"] = event["id"]
            properties["geometry"] = event["geometry"]
            cleandata.append(properties)
        else:
            messages += "Unexpected event type " + event["type"] + "\n"

    logger.debug(messages)

    return cleandata


@ app.route('/test', strict_slashes=False)
def test():
    return "confirming, test ok"


@ app.route('/health', strict_slashes=False)
def health():
    status = dict()

    if (eventdata != None):
        status['event-data'] = len(eventdata)
    status['config'] = config

    json = json.dumps(status, indent=2, sort_keys=False)
    logger.debug(json)
    return json


@app.route('/metadata', strict_slashes=False)
def getmetadata():
    return metadata


def stringelement(properties, testvalue, attributename):
    result = False
    value = properties[attributename]
    if (value != None) and (testvalue != None):
        value = str(value)
        value = value.lower()
        testvalue = str(testvalue)
        testvalue = testvalue.lower()

        result = (testvalue == value)

    return result


def booleanelement(properties, testvalue, attributename):
    result = False
    value = properties[attributename]
    if (value != None) and (testvalue != None):
        value = str(value)
        value = value.lower()
        testvalue = str(testvalue)
        testvalue = testvalue.lower()
        if (testvalue == "true"):
            testvalue = "1"
        if (testvalue == "false"):
            testvalue = "0"

        logger.debug("valuating %s against %s for %s",
                     attributename, testvalue, str(value))
        result = (testvalue == value)

    return result


def numericelement(properties, testvalue, attributename):
    result = False
    actualattributename = attributename
    if attributename in operatorcriteriamap:
        actualattributename = operatorcriteriamap[attributename]

    value = properties[actualattributename]
    if (value != None) and (testvalue != None):
        try:
            value = Decimal(value)
            testvalue = Decimal(testvalue)

        except ValueError:
            logger.debug("Value not numeric " +
                         str(value) + " or " + testvalue)

        if attributename.startswith("min"):
            result = (value <= testvalue)
        elif attributename.startswith("max"):
            result = (value >= testvalue)
        else:
            result = (value == testvalue)

    return result


operatorcriteriamap = {"mintime": "time",
                       "maxtime": "time",
                       "minmag": "mag",
                       "maxmag": "mag"}

criteriamap = {"mintime": numericelement,
               "maxtime": numericelement,
               "time": numericelement,
               "tsunami": booleanelement,
               "status": stringelement,
               "magtype": stringelement,
               "type": stringelement,
               "minmag": numericelement,
               "maxmag": numericelement,
               "mag": numericelement,
               "magType": stringelement,
               "alert": stringelement, }


@app.route('/event', methods=['GET'], strict_slashes=False)
def getevent():
    logger.debug("Get event - args are %s", str(request.args))
    response_code = 404

    matched_event = None
    event_id = ''
    if (request.args != None) and (len(request.args) > 0) and "id" in request.args:
        event_id = request.args.get('id')
        for event in eventdata:
            logger.debug("comparing %s and %s", event_id, event['id'])
            if (event['id'] != None) and (event['id'] == event_id):
                matched_event = str(event)
                response_code = 200
                break

    else:
        logger.debug("No id set - returning 204 with empty string")
        response_code = 404

    responsestr = ""
    if (matched_event != None) and len(matched_event) > 0:
        matched_event = "{'event': " + matched_event+"}"
        responsestr = json.dumps(matched_event, indent=2, sort_keys=True)
    else:
        logger.info("No Id match for " + event_id)
        responsestr = ''

    response = Response(response=responsestr,
                        status=response_code,
                        content_type="application/json")
    logger.debug("Returning response:" + responsestr)
    logger.debug("Returning response object:" + str(response))

    return response


@app.route('/event', methods=['DELETE'], strict_slashes=False)
def deleteevent():
    logger.debug("delete event - args are %s", str(request.args))
    response = Response()

    response_code = 410
    event_id = ''
    if (request.args != None) and (len(request.args) > 0) and "id" in request.args:
        # special case
        event_id = request.args['id']
        for event in eventdata:
            if (event['id'] != None) and (event['id'] == event_id):
                eventdata.remove(event)
                response_code = 200
                break
    else:
        logger.debug("No delete criteria set returning everything")

    logger.debug(response)
    return response, response_code


def matchlisttostring(matchedevents):
    responsestr = ""
    if len(matchedevents) > 0:
        responsestr = json.dumps(matchedevents, indent=2, sort_keys=True)

    return responsestr


def createsearchcriteria(args):
    searchcriteria = None

    if (args != None) and (len(args) > 0):
        # build the search criteria
        for arg in args:
            #logger.debug("arg evaluating " + arg)
            if searchcriteria == None:
                searchcriteria = dict()

            searchcriteria[arg] = args.get(arg)

    logger.debug("Search criteria is %s", str(searchcriteria))
    return searchcriteria


def applycriteria(searchcriteria, properties):
    matched = True
    for criteria in searchcriteria:
        if criteria in criteriamap:
            matched = criteriamap[criteria](
                properties, searchcriteria.get(criteria), criteria)
        else:
            logger.warning("unknown search criteria - " + criteria)
        if matched == False:
            break
            # didn't fail any of the search criteria

    return matched


@app.route('/events', methods=['GET'], strict_slashes=False)
def getevents():
    logger.debug("Get events - args are %s", str(request.args))

    matchedevents = list()
    searchcriteria = createsearchcriteria(request.args)

    if searchcriteria != None:
        # examine each event
        for event in eventdata:
            if (applycriteria(searchcriteria, event)):
                logger.debug("match for " + str(event))
                matchedevents.append(event)

    else:
        logger.debug("No search criteria set returning everything")
        matchedevents = eventdata

    logger.debug("Get events found %d matches", len(matchedevents))
    responsestr = matchlisttostring(matchedevents)
    logger.debug(responsestr)

    return responsestr


@app.route('/latestEvent', methods=['GET'], strict_slashes=False)
def get_latest_event():
    logger.debug("Get latest event ")

    latest_event = None
    latest_event_dtg = None

    for event in eventdata:
        current_event_dtg = event.get('time')
        if (current_event_dtg != None):
            if (latest_event_dtg == None) or (current_event_dtg > latest_event_dtg):
                latest_event_dtg = current_event_dtg
                latest_event = event

    responsestr = str(latest_event)
    logger.debug(responsestr)

    return (responsestr)


@ app.route('/raw', methods=['GET'], strict_slashes=False)
def raw():
    pretty_str = json.dumps(eventdata, indent=2, sort_keys=True)
    logger.debug(pretty_str)
    logger.debug("Record count="+str(len(eventdata)))
    return (pretty_str)


@app.errorhandler(404)
def page_not_found(error):
    logger.warning("Error handler caught request : %s", str(request.data))
    return 'URL not found', 404

# start the app up


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
eventdata = loaddata(config)
metadata = extractmetadata(eventdata)
eventdata = cleansedata(eventdata)
metadata = None
pretty_events_str = json.dumps(eventdata, indent=2, sort_keys=True)

logger.debug("Cleansing data:" + pretty_events_str)
logger.debug("==========")
logger.debug("Cleansing metadata data:" + str(metadata))
logger.debug("========== ready ==========")

if __name__ == '__main__':
    app.run(debug=config.getint('server', 'debug'),
            port=config.getint('server', 'port'),
            host=config.get('server', 'host'))
