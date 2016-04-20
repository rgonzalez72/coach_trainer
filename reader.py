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

        recordList.append (newRecord)

    for c in recordList:
        print c.getTitle ()
        print c.getEnergySystem ()




if __name__ == "__main__":
   readFile (sys.argv[1]) 
