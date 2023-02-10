import pandas as pd
import collections
import csv

# PART 1
# itr = pd.read_stata('uspatentcitation.dta', iterator=True)

# reader = csv.reader(open('sample_data.csv'),delimiter=',')


index = 0
patents = collections.defaultdict(list)  # {citation_id : [patent_id,category]}
issuedDateTable = {}
with open("sample_data.csv", "r") as file:
    reader = csv.reader(file)
    for curr in reader:
        # get issued_date based on citation_id
        if curr[2] not in issuedDateTable:
            issuedDateTable[curr[2]] = curr[3]

        if curr[7] == "":
            continue
        info = [curr[1], curr[7]]
        patents[curr[2]].append(info)

       

print((patents.keys()))

def findApplicantNum(lst):
    ans = 0
    for _,v in lst:
        if v == 'cited by applicant':
            ans += 1
    return ans
with open('table1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['patent_id', 'issued_date', '# of citations made_all',
                    '# of citations made_applicant', 'year', '# of citations received'])
    for patent, data in patents.items():
        count = {}  # {year XXXX : [applicantCount, totalThisYear]}
        writer.writerow(["A"])
        for d in data:
            if d[0] not in issuedDateTable:
                continue
            year_xxxx = int(issuedDateTable[d[0]][-2:])
            print(year_xxxx)
            if year_xxxx not in count:
                # applicantCount, totalThisYear
                count[year_xxxx] = [0, 0]
            temp = count[year_xxxx]
            # print(temp)
            
            temp[1] += 1
            count[year_xxxx] = temp

        yearOrder = sorted(count.items())
        if not yearOrder:
            continue
        start = yearOrder[0][0]
        end = yearOrder[-1][0]
        applicantNum = findApplicantNum(data)
        for year in range(start, end):
            if year in count:
                writer.writerow([patent, issuedDateTable[patent], len(
                    data), applicantNum, year, count[year][1]])
            else:
                writer.writerow(
                    [patent, issuedDateTable[patent], len(data), applicantNum, year, 0])


# PART 2
# itr = pd.read_stata('patnum_permco_1976_2021.dta', iterator = True)
# data = itr.get_chunk(5)
# index = 0

# companies = collections.defaultdict(list)
# for curr in itr:
#     # print(curr)
#     # print("RZ",len(curr),curr['patnum'])

#     # print(type(curr),type(curr["patnum"]),type(curr["patnum"]))
#     companyInfo = [curr["patnum"],curr["fdate"],curr["idate"],curr["year"]]
#     companies[curr["permco"]].append(companyInfo)

#     index += 1
#     if index == 5: break

# print(companies)
