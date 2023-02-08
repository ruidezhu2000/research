import pandas as pd
import collections
import csv

# PART 1
itr = pd.read_stata('uspatentcitation.dta', iterator = True)
# data = itr.get_chunk(5)
index = 0
patents = collections.defaultdict(list)
issuedDateTable = {}
for curr in itr:
    if curr["category"].values.item(0) == "": 
        continue

    # get issued_date 
    if curr["patent_id"].values.item(0) not in issuedDateTable:
        issuedDateTable[curr["patent_id"].values.item(0)] = curr["date"].values.item(0)

    info = [int(curr["date"].values.item(0)[:4]),curr["category"].values.item(0)]
    patents[curr["patent_id"].values.item(0)].append(info)
    
    # stopper
    index += 1
    if index == 50000: break
# print(patents)

# fake data for testing 
# patents = {'10456544': [[1943, 'cited by applicant'],[1943, 'cited by applicant'],[1944, 'cited by applicant']], '8250307': [[2008, 'cited by other']], 'D490798': [[1961, 'cited by examiner']], '9199394': [[1993, 'cited by applicant']], '10796471': [[2010, 'cited by applicant']]}

with open('table1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['patent_id', 'issued_date', '# of citations made_all', '# of citations made_applicant', 'year', '# of citations received'])
    for patent,data in patents.items():
        count = {}
        
        for d in data:
            # print("d:",d)
            # print(d.)
            if d[0] not in count: 
                count[d[0]] = [0,0] #applicantCount, totalThisYear
            temp = count[d[0]]
            # print(temp)
            if d[1] == 'cited by applicant':
                temp[0] += 1
            temp[1] += 1
            count[d[0]] = temp
        yearOrder = sorted(count.items())
        for year in yearOrder:
            # print("year:",year[0])
            writer.writerow([patent,issuedDateTable[patent], len(data),year[1][0], year[0], year[1][1]])


# PART 2
# itr = pd.read_stata('patnum_permco_1976_2021.dta', iterator = True)
# data = itr.get_chunk(5)
# index = 0

# companies = collections.defaultdict(list)
# for curr in itr:
#     # print(curr)
#     # print("RZ",len(curr),curr['patnum'])
    
#     # print(type(curr),type(curr["patnum"]),type(curr["patnum"].values.item(0)))
#     companyInfo = [curr["patnum"].values.item(0),curr["fdate"].values.item(0),curr["idate"].values.item(0),curr["year"].values.item(0)]
#     companies[curr["permco"].values.item(0)].append(companyInfo)

#     index += 1
#     if index == 5: break

# print(companies)


    