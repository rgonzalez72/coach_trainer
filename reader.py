#! /usr/bin/env python

import sys 
import os
from xml.dom import minidom
import datetime

class RecordException (Exception):
    def __init__ (self, msg):
        self._msg = msg

    def __str__ (self):
        return self._msg

class Record (object):

    E_SYSTEM_ALACTIC = "Alactic"
    E_SYSTEM_LACTIC = "Lactic"
    E_SYSTEM_AEROBIC = "Aerobic"

    E_SYSTEMS = [ E_SYSTEM_ALACTIC, E_SYSTEM_LACTIC, E_SYSTEM_AEROBIC]

    L_LOW = "Low"
    L_MEDIUM = "Medium"
    L_HIGH = "High"

    LOAD_TYPES = [L_LOW, L_MEDIUM, L_HIGH]

    def __init__ (self):
        self._date = None 
        self._title = None
        self._emphasis = None
        self._esystem = None
        self._load = None
        self._done = False
        self._tired = None
        self._motivation = None
        self._session = None
        self._distance = None
        self._atired = None

    def setDate (self, dateStr):   
        self._date = datetime.datetime.strptime (dateStr, "%d-%B-%Y")

    def getDate (self):    
        return self._date

    def setTitle (self, title):    
        self._title = title

    def getTitle (self):    
        return self._title

    def setEmphasis (self, emphasis):    
        self._emphasis = emphasis

    def getEmphasis (self):    
        return self._emphasis

    def setEnergySystem (self, esystem):    
        systemList = []

        # More than one system separated by /
        parts = esystem.split ("/")
        for p in parts:
            found = False
            for e in Record.E_SYSTEMS:
                if e.upper () == p.upper ():
                    found = True
                    systemList.append (e)
                    break

            if not found:         
                e = RecordException ("Invalid energy system " + p )
                raise e
        
        self._esystem = systemList        



    def getEnergySystem (self):    
        return self._esystem

    def setLoad (self, load):    
        loadList = []

        # More than one system separated by /
        parts = load.split ("/")
        for p in parts:
            found = False
            for e in Record.LOAD_TYPES:
                if e.upper () == p.upper ():
                    found = True
                    loadList.append (e)
                    break

            if not found:         
                e = RecordException ("Invalid energy system " + p )
                raise e
        
        self._load = loadList        

    def getLoad (self):    
        return self._load

    def setDone (self, done):    
        if done.upper() == "TRUE" or done.upper () == "YES":
            self._done = True
        else:
            self._done = False

    def getDone (self):    
        return self._done

    def setTired (self, tired):    
        tiredNum = int (tired)
        if tiredNum >= 0 and tiredNum <= 10:
            self._tired = tiredNum
        else:
            raise RecordException ("Invalid tired number " + str(tired))
    def getTired (self):    
        return self._tired

    def setMotivation (self, mot):    
        motNum = int (mot)
        if motNum >= 0 and motNum <= 10:
            self._motivation = motNum
        else:
            raise RecordException ("Invalid motivation number " + str(mot))

    def getMotivation (self):    
        return self._motivation

    def setSession (self, session):
        self._session  = session

    def getSession (self):    
        return self._session

    def setDistance (self, distance):    
        dist = float (distance)
        if dist >= 0.0 and dist < 100.0:
            self._distance = distance
        else:
            raise RecordException ("Invalid distance " + str(distance))

    def getDistance (self):    
        return self._distance

    def setATired (self, tired):    
        tiredNum = int (tired)
        if tiredNum >= 0 and tiredNum <= 10:
            self._atired = tiredNum
        else:
            raise RecordException ("Invalid tired number " + str(tired))

    def getATired (self):    
        return self._atired

def readFile (fileName):
    xmldoc = minidom.parse (fileName)
    dataObject = xmldoc.getElementsByTagName ('data')
    name = dataObject[0].getElementsByTagName ('name')
    nameStr = None
    for c in name[0].childNodes:
        nameStr =  c.data

    recordsList = dataObject[0].getElementsByTagName ('records')
    
    records = recordsList[0].getElementsByTagName ('record')

    recordList = []
    
    for c in records:
        newRecord = Record ()

        date = c.getElementsByTagName ('date')
        newRecord.setDate ( date[0].childNodes [0].data)

        title = c.getElementsByTagName ('title')
        newRecord.setTitle (title[0].childNodes[0].data)

        emp = c.getElementsByTagName ('emphasis')
        if len (emp[0].childNodes) > 0:
            newRecord.setEmphasis (emp[0].childNodes[0].data)

        es = c.getElementsByTagName ("esystem")
        if len (es[0].childNodes) > 0:
            newRecord.setEnergySystem (es[0].childNodes[0].data)

        load = c.getElementsByTagName ("load")
        if len (load[0].childNodes) > 0:
            newRecord.setLoad (load[0].childNodes[0].data)

        done = c.getElementsByTagName ("done")
        if len (done[0].childNodes) > 0:
            newRecord.setDone (done[0].childNodes[0].data)

        tired = c.getElementsByTagName ("tired")
        if len (tired[0].childNodes) > 0:
            newRecord.setTired (tired[0].childNodes[0].data)

        mot = c.getElementsByTagName ("motivation")
        if len (mot[0].childNodes) > 0:
            newRecord.setMotivation (mot[0].childNodes[0].data)

        session = c.getElementsByTagName ("session")
        if len (session[0].childNodes) > 0:
            newRecord.setSession (session[0].childNodes[0].data)

        dist = c.getElementsByTagName ("distance")
        if len (dist[0].childNodes) > 0:
            newRecord.setDistance (dist[0].childNodes[0].data)

        atired = c.getElementsByTagName ("atired")
        if len (atired[0].childNodes) > 0:
            newRecord.setATired (atired[0].childNodes[0].data)

        recordList.append (newRecord)

    for c in recordList:
        print c.getTitle ()
        print c.getATired ()




if __name__ == "__main__":
   readFile (sys.argv[1]) 
