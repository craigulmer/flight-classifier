
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
    'emergency':'red',
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
    times.parseDumpFile()
    icao.load()
    faa.load(flight_ids=times.getFlights())
    cats.load()

    for id in times.getFlights():
        o = faa.getOwner(id)
        c = cats.getCategory(o)
        p = icao.getCountry(id)
        times.setOwner(id, o)
        times.setClassification(id, c)
        times.setCountry(id, p)
else:
    # Or, accept the cooked results from something already analyzed
    times.parseCookedFile(fn=fn_cooked)



plt.figure(figsize=(12,8))

airtimes=[]
axes={} # dumb.. store all the axes we've plotted to retain colors
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
    ax = plt.plot(x,y, linewidth=line_width,color=colors[c])
    if(not c in axes):
        axes[c]=ax
    spot=spot+1

    print times.getFullInfo(id)


plt.gcf().autofmt_xdate()
plt.gca().yaxis.set_major_formatter(plt.NullFormatter())

# Yuck. Force the category names to be plotted in specific order. We have
# to retrieve each one's handle to make sure we link the bar color right
names=['passenger','private charter','bank','oil','emergency','unclassified']
handles=[]
for i in names:
    handles.append(axes[i])

print handles
print names
#plt.legend(handles=handles,labels=names, loc='upper left')
#plt.legend()
plt.title("Flight Timeline")
plt.show()

plt.figure(figsize=(10,5))
plt.hist(airtimes, bins=30)
plt.title("Airtime Historgram")
plt.xlabel("In-Air Time (Seconds)")
plt.ylabel("Plane Counts")
plt.show()

#plt.plot(x,y)
#plt.gcf().autofmt_xdate()

#plt.show()
