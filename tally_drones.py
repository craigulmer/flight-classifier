# This script is used to parse an FAA master database file
# to pull out drone counts for different organizations. You
# can filter by whether its a gov/commercial entity, as
# well as by owner name.
#
# This is a one time script, so I didn't bother to put an
# arg parser on this. Just edit the top globals to change
# things.

import operator

fn = "data/MASTER.txt"
limit_num= 0 #200  #limit how many items to plot from file

org_filter = "none" # business, gov, govplus, none

#owner_keywords=["LOCKHEED"]
#owner_keywords=["UNIVERSITY", "INSTITUTE", "COLLEGE"]
#owner_keywords=["NATIONAL"]
#owner_keywords=["LABORATORY", "LABORATORIES"] 
owner_keywords=[]


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
#        10=Electric, 6=ramjet, 4=turbojet


possible_org_filers = { "business":["3","4","8","9"],
                        "gov":     ["5"],
                        "govplus": ["1", "2","3","4","5","8","9"],
                        "none":    []}

filter=possible_org_filers[org_filter]
owners={}
ids={}
num_found=0

with open(fn) as f:
    for line in f:
        csv=line.split(',')
        aid=csv[33].rstrip()
        rname=csv[6].rstrip()
        rtype=csv[5].rstrip()
        etype=csv[19].rstrip()
        idate=csv[16].rstrip()
        alt_name=csv[24].rstrip()

        tailfin=csv[0].rstrip()
        
        #Yuck.. sometimes people put name in alt_name. Pipe together, 
        #so we have a better chance of filters working in next phase
        if alt_name != "":
            name=rname+" | "+alt_name;
        else:
            name=rname

        if etype=="10" and ((len(filter)==0) or (rtype in filter)) : 

            #print tailfin+" "+idate
            if not name in owners:
                owners[name]=1
            else:
                owners[name]=owners[name]+1

            if limit_num>0 and num_found>=limit_num:
                break
            num_found=num_found+1

sorted_owners = sorted(owners.items(), key=operator.itemgetter(1),reverse=True) 

#filters=["LOCKHEED"]
#filters=["UNIVERSITY", "INSTITUTE", "COLLEGE"]
#filters=["NATIONAL"]
#filters=["LABORATORY", "LABORATORIES"] 
#filters=[]
num=0
for k,v in sorted_owners: #sorted_owners[:20]:
    if len(owner_keywords)==0:
        found=True
    else:
        terms=k.split()
        found=False
        for t in terms:
            if t in owner_keywords:
                #print "%4d    %s" %(v,k.title())
                #num=num+1
                found=True
                break

    if found:
        print "%4d    %s" %(v,k.title())

#for k,v in sorted_owners: #sorted_owners[:20]:
#    print "%4d    %s" %(v,k.title())
        
