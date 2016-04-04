
import time



import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from datetime import datetime,date


import planemeta as pm

# Global settings
line_width=3.0
fn_cooked = "cooked.txt"

colors = {
    'passenger':'blue',
    'private charter' : 'darkblue',
    'emergency':'purple',
    'surveillance': 'red',
    'bank' : 'green',
    'oil' : 'black',
    'realestate':'dimgray',
    'gun':'darkslategray',
    'trucking':'darkgray',
    'unclassified':'gray',
    'unknown':'magenta'
}

times = pm.StartStops()
icao = pm.ICAOLookup()
faa = pm.FAAInfoLookup()
cats = pm.OwnerCategories()

# From Scratch: load everything
if (fn_cooked==""):
    times.parseDumpFile("data/superbowl_nc.txt")
    icao.load()
    faa.load(flight_ids=times.getFlights())
    cats.load()

    for id in times.getFlights():
        o = faa.getOwner(id)
        c = cats.getCategory(o)
        p = icao.getCountry(id)
        if p=="(reserved, EUR/NAT)":
            o = "surveillance"
            c = "surveillance"
        times.setOwner(id, o)
        times.setClassification(id, c)
        times.setCountry(id, p)
        
else:
    # Or, accept the cooked results from something already analyzed
    times.parseCookedFile(fn=fn_cooked)



plt.figure(figsize=(12,8))


airtimes=[]
spot=0
#for k,v in starts.iteritems():

sorted_ids = times.getFlightsSortedByStart()
for (id,t) in sorted_ids:
    x=times.getTimesAsDates(id)
    y=[spot, spot]
    c=times.getClassification(id)

    #python 2.6 was missing timedelta.total_seconds()
    dt = times.getAirTime(id)
    num_secs = ((dt.seconds+dt.days*24*3600)*10**6)/10**6

    airtimes.append(num_secs)
    plt.plot(x,y, linewidth=line_width,color=colors[c], label=c)

    spot=spot+1

    print times.getFullInfo(id)


plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%I:%M:%S %p"))
plt.gca().yaxis.set_major_formatter(plt.NullFormatter())

# Yuck. Force the category names to be plotted in specific order. We have
# to retrieve each one's handle to make sure we link the bar color right
names=['passenger','private charter','bank','oil','emergency','surveillance','unclassified']
hh,ll=plt.gca().get_legend_handles_labels()
handles=[]
for n in names:
    handles.append(hh[ ll.index(n) ])


# get_label()

#print handles
#print names

plt.legend(handles=handles,labels=names, loc='upper left')
#plt.legend()
plt.title("Flight Timeline")
plt.show()


for i in range(len(airtimes)):
    airtimes[i] = airtimes[i]/60.0

plt.figure(figsize=(10,5))
plt.hist(airtimes, bins=30)
plt.title("Airtime Historgram")
plt.xlabel("In-Air Time (Minutes)")
plt.ylabel("Plane Counts")
plt.show()

#plt.plot(x,y)
#plt.gcf().autofmt_xdate()

#plt.show()
