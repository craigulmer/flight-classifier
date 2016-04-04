
import time
import operator
from datetime import datetime,date


class ICAOLookup:
    icao_country_ranges=[]
    def load(self, filename="data/all_icao_country_codes.txt"):
        with open(filename) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                csv=line.rstrip().split('\t')
                self.icao_country_ranges.append(csv)
                #print csv[0]+"|"+csv[1]+"|"+csv[2]+"|"
                # Make sure it's in order
        self.icao_country_ranges.sort()

    def getCountry(self, hex_id ):
        for x in self.icao_country_ranges:
            if (hex_id >= x[0]) and (hex_id <= x[1]):
                return x[2]
        return "unknown"


class FAAInfoLookup:
    registrations={}

    # Parse the master faa file and lookup planes using the 7th and 34th cols
    # note: throws a lot of data away, may be better to awk it out
    def load(self, fn="data/MASTER.txt", flight_ids=[]):
        with open(fn) as f:
            f.readline() # first line is meta, skip it
            for line in f:
                csv=line.rstrip().split(',')
                id=csv[33].rstrip()
                if (not flight_ids) or (id in flight_ids):
                    if len(csv)>1:
                        owner = csv[6].rstrip()
                    else:
                        owner = ""
                    self.registrations[id]=owner

    def makeCooked(self, fn="data/MASTER.txt"):
        with open(fn) as f:
            for line in f:
               csv=line.rstrip().split(',')
               id=csv[33].rstrip()
               owner=csv[6].rstrip()
               print id+"\t"+owner

    def loadCooked(self, fn="data/MASTER_aid_owner.txt", flight_ids=[]):
        with open(fn) as f:
            f.readline() # First line is meta, skip it
            for line in f:
                csv=line.rstrip().split('\t')
                id = csv[0]
                
                if (not flight_ids) or (id in flight_ids):
                    #print id,"\t",csv[1]
                    if len(csv)>1:
                        owner = csv[1].rstrip()
                    else:
                        owner = ""
                    self.registrations[id]=owner
                    #print id+"\t"+cat+"\t"+owner_info            
                    #print csv[1]
                    #print line 

    def getOwner(self,id):
        if(id in self.registrations):
            return self.registrations[id]
        else:
            return "unknown\t"


class OwnerCategories:
    cats={}
    subcats={}
    def load(self, fn="data/cdu_plane_categories.txt"):
        with open(fn) as f:
            for line in f:
                if line.startswith('#'):
                    continue  
                csv=line.rstrip().split('\t')
                #print "Cat is "+csv[0]
                owner=csv[2].rstrip()
                self.cats[owner] = csv[0].rstrip()
                self.subcats[owner] = csv[1].rstrip()

    def getCategory(self, owner):
        if (owner in self.cats):
            return self.cats[owner]
        else:
            return "unclassified"

    def getSubCategory(self, owner):
        if(owner in self.substas):
            return self.subcats[owner]
        else:
            return "unclassified"

    def dump(self):
        for i in self.cats:
            print "'"+i+"' ---> '"+self.cats[i]+"'"


class StartStops():
    starts={}
    stops={}
    countries={}
    classifications={}
    owners={}

    def parseDumpFile(self, fn="data/superbowl_nc.txt"):
        ids=set()
        with open(fn) as f:
            for line in f:
                csv=line.split(',')
                id=csv[4]
                time=csv[8]+" "+csv[9]
                flt=csv[10]

                if id in ids:
                    self.stops[id]=time
                else:
                    self.starts[id]=time
                    self.stops[id]=time
                    ids.add(id)        

    # If previously parsed a file, we can reload the 
    # cooked results directly and use it. This avoids a lot
    # of extra parsing, but you're also stuck with whatever
    # the classifications were at parse time.
    def parseCookedFile(self, fn="data/start_stop.txt"):
        with open(fn) as f:
            for line in f:
                csv=line.rstrip().split('\t')
                id = csv[0].rstrip()
                self.starts[id] = csv[1]
                self.stops[id]  = csv[2]
                self.countries[id] = csv[3]
                self.classifications[id] = csv[4]
                self.owners[id] = csv[5]

    def getAirTime(self, id):
        return self.getStopAsDate(id) - self.getStartAsDate(id)

    def getStartStop(self, id):
        return self.starts[id]+"\t"+self.stops[id]
    
    def getStart(self, id):
        return self.starts[id]

    def getStop(self, id):
        return self.stops[id]

    def getFlights(self):
        return self.starts.keys()

    def getFlightsSortedByStart(self):
        return sorted(self.starts.items(), key=operator.itemgetter(1))

    def setCountry(self, id, country):
        self.countries[id]=country

    def getCountry(self, id):
        if (id in self.countries):
            return self.countries[id]
        return "unknown"

    def setClassification(self, id, classification):
        self.classifications[id]=classification

    def getClassification(self, id):
        if (id in self.classifications):
            return self.classifications[id]
        return "unclassified"

    def setOwner(self, id, owner):
        self.owners[id]=owner
    def getOwner(self, id):
        if (id in self.owners):
            return self.owners[id]
        return ""

    def getStartAsDate(self,id):
        return datetime.strptime(self.starts[id].rstrip(),"%Y/%m/%d %H:%M:%S.%f")

    def getStopAsDate(self,id):
        return datetime.strptime(self.stops[id].rstrip(),"%Y/%m/%d %H:%M:%S.%f")

    def getTimesAsDates(self, id):        
        d1 = self.getStartAsDate(id)
        d2 = self.getStopAsDate(id)
        return [d1,d2]

    def getFullInfo(self, id):
        return "%s\t%s\t%s\t%s\t%s\t%s" % (
            id, 
            self.getStart(id),
            self.getStop(id),
            self.getCountry(id), 
            self.getClassification(id), 
            self.getOwner(id))
