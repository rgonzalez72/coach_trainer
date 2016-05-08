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
                e = RecordException ("Invalid load " + p )
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
            self._distance = float (distance)
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

    def getLoadStr (self):    
        loadStr = ""
        index = 0
        for l in self._load:
            if index > 0:
                loadStr +="/"
            loadStr += l
            index += 1

        return loadStr

    def getEmphasisStr (self):    
        empStr = ""
        index = 0
        if self._esystem is not None:
            for l in self._esystem:
                if index > 0:
                    empStr +="/"
                empStr += l
                index += 1

        return empStr

    def printDetailedSession (self, fp):    
        fp.write ("\n")
        fp.write ( self._date.strftime ("%A, %d-%B-%Y") + "\n")
        fp.write ( self._title + "\n")
        fp.write ("Load: " + str(self.getLoadStr()) + ", emphasis: " + 
                str(self._emphasis) + ", energy system: " + 
                str(self.getEmphasisStr ()) +".\n")

    @staticmethod 
    def ktomile (k):
        return k/1.609

class Week (object):        

    def __init__ (self):
        self._load = None
        self._sessions = []

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
                e = RecordException ("Invalid load " + p )
                raise e
        
        self._load = loadList        

    def getLoad (self):    
        return self._load 

    def addSession (self, session):    
        self._sessions.append (session)

    def getFirstDate (self):    
        return self._sessions[0].getDate ()

    def getNumberOfSessions (self):    
        return len (self._sessions)

    def printDetailedWeek (self, fp):    
        for s in self._sessions:
            s.printDetailedSession (fp)

    def getDistance (self):
        distance = 0.0
        for s in self._sessions:
            if s.getDone ():
                distance += s.getDistance ()
        return distance

    def getDone (self):
        done=0
        for s in self._sessions:
            if s.getDone ():
                done += 1
        return done

class TestPlan (object):        

    def __init__ (self):
        self._name = None
        self._weeks = []

    def setName (self, name):    
        self._name = name

    def getName (self):    
        return self._name

    def addWeek (self, week):
        self._weeks.append (week)

    def printSummary (self, outFileName):    
        with open (outFileName, "w") as fp:
            fp.write ("Test plan for " + self.getName () + ".\n")
            fp.write ("The plan consists of " + str(len (self._weeks)) + " weeks.\n\n")


            index = 1
            for w in self._weeks:
                fp.write ("Week " + str(index) + ", load " + w.getLoad ()[0] + ", date " + \
                        w.getFirstDate().strftime ("%A, %d-%B-%Y") + ", " + \
                        str(w.getNumberOfSessions ()) + " sessions.\n")
                if w.getDone () > 0:
                    distance =w.getDistance ()
                    fp.write ("\tTotal distance: " + str(distance) + "k/" + 
                            "%0.2f" % Record.ktomile (distance) + "m\n")

                index += 1

    def printDetailedPlan (self, outFileName):                
        with open (outFileName, "w") as fp:
            fp.write ("Test plan for " + self.getName () + ".\n")
            fp.write ("The plan consists of " + str(len (self._weeks)) + " weeks.\n\n")

            index = 1
            for w in self._weeks:
                fp.write ("\n\nWeek " + str(index) + ", load " + w.getLoad ()[0] + ".\n") 
                w.printDetailedWeek (fp)

                index += 1           

    def printHeader (self, fp, title):
        fp.write ("<html>\n")
        fp.write ("<head>\n")
        fp.write ("<title>" + title + "</title>\n")
        fp.write ("</head>\n")
        fp.write ("<body>\n")
        fp.write ("\t<h2>"+ title + "</h2>\n")

    def printFooter (self, fp):
        fp.write ("</body>\n")
        fp.write ("</html>\n")

    def printBody (self, fp):
        fp.write ("\t<p>The plan consists of " + str(len (self._weeks)) + " weeks.</p>\n")
        index = 1
        for w in self._weeks:
            fp.write ('\t<p><table border="1">')
            fp.write ('\t\t<tr><th colspan="8">' + "aaaa" + "</th></tr>\n")
            fp.write ('\t\t<tr><td>Days<td>Monday</td><Tuesday></td><td>Wednesday</td>' + 
                    "<td>Thursday</td><td>Friday</td><td>Saturday</td><td>Sunday</td></tr>\n")
            fp.write ("\t</table><p>\n")

    def printDetailedPlanHTML (self, outFileName):
        with open (outFileName, "w") as fp:
            title = "Test plan for " + self.getName () 
            self.printHeader (fp, title)
            self.printBody (fp)
            self.printFooter (fp)
            

def readFile (fileName):
    TP = TestPlan ()
    xmldoc = minidom.parse (fileName)
    dataObject = xmldoc.getElementsByTagName ('data')
    name = dataObject[0].getElementsByTagName ('name')
    nameStr = None
    for c in name[0].childNodes:
        nameStr =  c.data

    TP.setName (nameStr)

    weekList = dataObject[0].getElementsByTagName ('weeks')
    weeks = weekList [0].getElementsByTagName ('week')


    for w in weeks:
        W = Week () 

        load = w.getElementsByTagName ('wload')
        W.setLoad (load[0].childNodes[0].data)

        recordsList = w.getElementsByTagName ('records')
    
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

            W.addSession (newRecord)
        TP.addWeek (W)

    return TP


if __name__ == "__main__":
    TP = readFile (sys.argv[1]) 
    TP.printSummary ("summary.txt") 
    TP.printDetailedPlan ("weeks.txt")
    TP.printDetailedPlanHTML ("weeks.html")
