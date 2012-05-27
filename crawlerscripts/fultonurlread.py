import urllib2
import html5lib
import re
import csv
from html5lib import treebuilders
from HTMLParser import HTMLParser
from time import sleep

home_url = "http://ga.state.gegov.com/georgia/inspectionPick.cfm?id="
def remove_spaces(string):
    string = re.sub('\s{2,}', ' ',string)
    return string
def remove_minus(string):
    string = re.sub('-', '',string)
    return string
def find_bold(string):
    beginning = string.find("<b>")
    end = string.find("</b>",beginning+1)
    return beginning

allvalues = []
#name output file
out = csv.writer(open("fulton.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)

#range of id's to iterate over
for i in range (889218,890000):
    sleep (10)
    req = urllib2.Request(home_url + str(i))
    try:
        response = urllib2.urlopen(req)
    except HTTPError:
        sleep(5)
        response = urllib2.urlopen(req)    
    the_page = response.read()
    if (the_page.find("<h3>")>0):
        pagelist = [i]
        
        
        starth = the_page.find("<h3>")
        endh = the_page.find("</h3>")
        pagelist.append(the_page[starth+4:endh])
      
        
        starta = the_page.find(";\">",endh)
        enda = the_page.find("</span>",starta+1)
        address = the_page[starta+3:enda]
        pagelist.append(remove_minus(remove_spaces(address)))
        
        
        if (the_page.find("Score:")>0):
            startd = the_page.find("county=",enda)
            endd = the_page.find("</a>", startd+9)
            pagelist.append(the_page[startd+9:endd])
           
                    
            starts = the_page.find("Score:")
            ends = the_page.find(",", starts+1)
            pagelist.append(the_page[starts+7:ends])
            allvalues.append(pagelist)
            
            
            startl = the_page.find("<a href=", starth)
            endl = the_page.find("\">",startl)
            pagelist.append("http://ga.state.gegov.com/georgia/"+ the_page[startl+9:endl])
           
    
        pagelist.append("Food")
        pagelist.append(home_url+str(i))
        pagelist.append("Fulton")
        out.writerow(pagelist)
        
        #shows the id's that have records
        print i
        
print "Finished"
