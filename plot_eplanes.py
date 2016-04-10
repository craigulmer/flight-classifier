from datetime import datetime,date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

fn = "data/MASTER.txt"
limit_num= 0 #200  #limit how many items to plot from file

def fmt_commas(val, pos=None):
    s = '%d' % val
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

def addToDateCount(the_list, the_date):
    if not the_date in the_list:
        the_list[the_date]=1
    else:
        the_list[the_date]=the_list[the_date]+1

def calcStats(the_list):
    days=[]
    counts=[]
    cumulatives=[]
    total_num=0
    for k in sorted(the_list):
        total_num=total_num+the_list[k]
        days.append(datetime.strptime(k,"%Y%m%d"))
        counts.append(the_list[k])
        cumulatives.append(total_num)
    return (days,counts,cumulatives)

#See http://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/media/ardata.pdf
# Reg Types: 
#        1=individual
#        2=partnership
#        3=Corporation
#        4=Co-Owned
#        5=Government
#        8=Non Citizen Corpo
#        9=Non Citizen Co-owned
# Eng Types
#        10=Electric, 6=ramjet


business=["3","4","8","9"]
gov=["5"]

owners={}
idates={}
idates_bus={}
idates_gov={}
idates_other={}
ids={}

with open(fn) as f:
    for line in f:
        csv=line.split(',')
        aid=csv[33].rstrip()
        name=csv[6].rstrip()
        rtype=csv[5].rstrip()
        etype=csv[19].rstrip()
        idate=csv[16].rstrip()
        
        if etype=="10":# and rtype in business : #True: #rtype=="3":

            #print idate
            if not name in owners:
                owners[name]=1
            else:
                owners[name]=owners[name]+1

            if idate!="":

                addToDateCount(idates, idate)
                if rtype in business:
                    addToDateCount(idates_bus, idate)
                elif rtype in gov:
                    addToDateCount(idates_gov, idate)
                else:
                    addToDateCount(idates_other, idate)

            if limit_num>0 and len(idates)>=limit_num:
                break
            

#for i in owners:
#    print owners[i],"\t",i


# For each category, generate times, dailycounts, and running counts
data={}
data["all"] = calcStats(idates)
data["gov"] = calcStats(idates_gov)
data["bus"] = calcStats(idates_bus)
data["other"] = calcStats(idates_other)

labels={ "all":"All",  "gov":"Government", "bus":"Business", "other":"Other"}
colors={ "all":"blue", "gov":"red", "bus":"black", "other":"green"}

plt.figure()
plt.subplot(211)
for id in ("all","bus","gov"):
    m,s,b=plt.stem(data[id][0], data[id][1], markerfmt=" ", label=labels[id]) 
    plt.setp(s,'color',colors[id],'linewidth',2)

plt.legend(loc="upper left", numpoints=1)
plt.title("Electric Plane Registrations per Day")



plt.subplot(212)
lw=2
for id in ("all","bus","gov","other"):
    ls="-"
    if id=="all": ls="--"
    plt.plot(data[id][0],data[id][2],
             label=labels[id],
             color=colors[id],
             linestyle=ls,
             linewidth=lw)

plt.legend(loc="upper left")
plt.gcf().autofmt_xdate()
plt.gcf().gca().yaxis.set_major_formatter(FuncFormatter(fmt_commas))
plt.title("Total Electric Planes")

plt.show()


