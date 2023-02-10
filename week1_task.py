import pandas as pd
import collections
import csv

# PART 1
itr = pd.read_stata('uspatentcitation.dta', iterator=True)
# itr = pd.read_stata('sample data.csv', iterator=True)
# data = itr.get_chunk(5)
index = 0
patents = collections.defaultdict(list)  # {citation_id : [patent_id,category]}
issuedDateTable = {}
for curr in itr:
    if curr["category"].values.item(0) == "":
        continue

    # get issued_date based on citation_id
    if curr["citation_id"].values.item(0) not in issuedDateTable:
        issuedDateTable[curr["citation_id"].values.item(
            0)] = curr["date"].values.item(0)

    info = [curr["patent_id"].values.item(0), curr["category"].values.item(0)]
    patents[curr["citation_id"].values.item(0)].append(info)

    # stopper
    index += 1
    if index == 50000:
        break

# print(patents)


with open('table1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['patent_id', 'issued_date', '# of citations made_all',
                    '# of citations made_applicant', 'year', '# of citations received'])
    for patent, data in patents.items():
        count = {}  # {year XXXX : [applicantCount, totalThisYear]}

        for d in data:
            if d[0] not in issuedDateTable:
                continue
            year_xxxx = int(issuedDateTable[d[0]][:4])
            if year_xxxx not in count:
                # applicantCount, totalThisYear
                count[year_xxxx] = [0, 0]
            temp = count[year_xxxx]
            # print(temp)
            if d[1] == 'cited by applicant':
                temp[0] += 1
            temp[1] += 1
            count[year_xxxx] = temp

        yearOrder = sorted(count.items())
        if not yearOrder:
            continue
        start = yearOrder[0][0]
        end = yearOrder[-1][0]

        for year in range(start, end):
            if year in count:
                writer.writerow([patent, issuedDateTable[patent], len(
                    data), count[year][0], year, count[year][1]])
            else:
                writer.writerow(
                    [patent, issuedDateTable[patent], len(data), 0, year, 0])


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
