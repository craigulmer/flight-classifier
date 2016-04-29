import sys
import getopt
import operator
import time

# NOTE: This needs a more recent version of python than came with
#       centos 6. I installed python 3.5, which worked fine.


#Geopy does the translation, but needs Python 2.8+
from geopy.geocoders import Nominatim


fn = "data/MASTER.txt"
limit_num= 0 #10 #200  #limit how many items to plot from file
geolookup=False
zipcode="94550"

def help():
    print("extract_by_zipcode.py <-g> <-z zipcode>\n"
              "   -g         : do additional lon/lat lookup\n"
              "   -z zipcode : search on this zipcode\n");
    sys.exit(0)


#---- Args --------------------------------------------------------------------
try:
    opts,args = getopt.getopt(sys.argv[1:], "gz:", ["geolookup","zipcode="])
except getopt.GetoptError:
    help()

for opt,arg in opts:
    if opt in ("-g", "--geolookup"):
        geolookup=True
    elif opt in ("-z", "--zipcode"):
        zipcode=arg
    else:
        help();

#------------------------------------------------------------------------------
addresses={}
num=0
with open(fn) as f:
    for line in f:
        #if not "LIVERMORE" in line:
        #    continue
 

        csv=line.split(',')
        aid=csv[33].rstrip()
        rname=csv[6].rstrip()
        rtype=csv[5].rstrip()
        etype=csv[19].rstrip()
        idate=csv[16].rstrip()
        alt_name=csv[24].rstrip()

        street=csv[7].rstrip()
        city=csv[9].rstrip()
        state=csv[10].rstrip()
        zip=csv[11].rstrip()[0:5]

        if street=="" or city=="" or state=="" or zip=="":
            continue

        if street.startswith("ATTN"):
            search_string = city+","+state+","+zip
        else:
            search_string = street+","+city+","+state+","+zip
      

        if zip==zipcode:        
        #if etype=="10": 
            #print(search_string)
            if search_string in addresses:
                addresses[search_string]=addresses[search_string]+1
            else:
                addresses[search_string]=1
            num=num+1

        if limit_num>0 and num>limit_num:
            break

if not geolookup:
    #Just dump the addresses
    for k in addresses:
        print("%d\t%s" % (addresses[k],k))

else:

    geolocator = Nominatim()

    for k in addresses: 

        location = geolocator.geocode(k)
        if location != None:
            print("%d\t%s\t%f\t%f" % (addresses[k], k, location.longitude, location.latitude))
        else:
            print("%d\t%s" % (addresses[k],k))

        time.sleep(3)
