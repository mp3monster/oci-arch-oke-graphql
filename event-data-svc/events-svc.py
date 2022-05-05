
# Copyright(c) 2022, Oracle and / or its affiliates.
# All rights reserved. The Universal Permissive License(UPL), Version 1.0 as shown at http: // oss.oracle.com/licenses/upl
#
# useful resources
# https://flask.palletsprojects.com/en/2.1.x/
#


from importlib.metadata import metadata
import json
from flask import Flask, request, Response
import configparser
from decimal import *


app = Flask(__name__)


def getconfig():
    config = configparser.RawConfigParser()
    config.read('event-svc.cfg')

    return config


def loaddata(config):

    # Opening JSON file
    filehandle = open(config.get('data', 'file'))
    eventdata = json.load(filehandle)
    filehandle.close()

    return eventdata

# separate the metadata record from the events


def extractmetadata(eventdata):
    for event in eventdata:
        if (event["type"] == "FeatureCollection"):
            return event
    return None


def cleansedata(eventdata):
    messages = ""
    for event in eventdata:
        if (event["type"] == "FeatureCollection"):
            eventdata.remove(event)
            messages += "Located meta data entry\n"
        elif (event["type"] != "Feature"):
            messages += "Unexpected event type " + event["type"] + "\n"
            eventdata.remove(event)
        else:
            event.pop("type")
    print(messages)

    return eventdata


@ app.route('/test/')
def test():
    return "hello world"


@app.route('/metadata/')
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
            print("Value not numeric " + str(value) + " or " + testvalue)

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


@app.route('/event', methods=['GET'])
def getevent():
    matchedevents = list()
    eventid = ""
    if (request.args != None) and (len(request.args) > 0) and "id" in request.args:
        # special case
        eventid = request.args['id']
        for event in eventdata:
            if (event['id'] != None) and (event['id'] == eventid):
                matchedevents.append(event)
                break

    else:
        print("No search criteria set returning everything")

    responsestr = ""
    if len(matchedevents) > 0:
        responsestr = json.dumps(matchedevents, indent=2, sort_keys=True)

    return responsestr


@app.route('/event', methods=['DELETE'])
def deleteevent():
    response = Response(status=410)
    eventid = ""
    if (request.args != None) and (len(request.args) > 0) and "id" in request.args:
        # special case
        eventid = request.args['id']
        for event in eventdata:
            if (event['id'] != None) and (event['id'] == eventid):
                eventdata.remove(event)
                response = Response(status=200)
                break
    else:
        print("No search criteria set returning everything")

    return response


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
            #print("arg evaluating " + arg)
            if searchcriteria == None:
                searchcriteria = dict()

            searchcriteria[arg] = args.get(arg)

    return searchcriteria


@app.route('/events/', methods=['GET'])
@app.route('/events', methods=['GET'])
def getevents():
    matchedevents = list()
    searchcriteria = createsearchcriteria(request.args)

    if searchcriteria != None:
        # examine each event
        for event in eventdata:
            matched = True
            properties = event.get('properties')
            for criteria in searchcriteria:
                if criteria in criteriamap:
                    matched = criteriamap[criteria](
                        properties, searchcriteria.get(criteria), criteria)
                else:
                    print("unknown search criteria - " + criteria)
                if matched == False:
                    break
            # didnt fail any of the search criteria
            if (matched):
                print("match for " + str(event))
                matchedevents.append(event)

    else:
        print("No search criteria set returning everything")
        matchedevents = eventdata

    return matchlisttostring(matchedevents)


@ app.route('/raw/')
def raw():
    pretty_str = json.dumps(eventdata, indent=2, sort_keys=True)
    print(pretty_str)
    print("Record count="+str(len(eventdata)))
    return (pretty_str)

# start the app up


config = getconfig()
os.environ['host'] = config.get('server', 'host')
os.environ['port'] = config.get('server', 'port')
eventdata = loaddata(config)
metadata = extractmetadata(eventdata)
eventdata = cleansedata(eventdata)
metadata = None
pretty_events_str = json.dumps(eventdata, indent=2, sort_keys=True)
pretty_metadata_str = json.dumps(metadata, indent=2, sort_keys=True)

print("Cleansing data:" + pretty_events_str)
print("==========")
print("Cleansing metadata data:" + pretty_metadata_str)


if __name__ == '__main__':
    app.run(debug=config.getint('server', 'debug'),
            port=config.getint('server', 'port'),
            host=config.get('server', 'host'))
