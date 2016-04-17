#! /usr/bin/env python

import sys 
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def readFile (fileName):
    xmldoc = minidom.parse (fileName)
    dataObject = xmldoc.getElementsByTagName ('data')
    name = dataObject[0].getElementsByTagName ('name')
    for c in name[0].childNodes:
        print c.data

    recordsList = dataObject[0].getElementsByTagName ('records')
    
    records = recordsList[0].getElementsByTagName ('record')
    
    print len (records)
    for c in records:
        date = c.getElementsByTagName ('date')
        print date[0].childNodes [0].data



"""def readFile (fileName):
    tree = ET.parse (fileName)
    root = tree.getroot ()
    for child in root:
        if child.tag == "name":
            print child.text
    for record in root.findall ("./records/record"):
                print record.tag"""

if __name__ == "__main__":
   readFile (sys.argv[1]) 
