# Aggregates all bill data into a master data set 
# Author: Kiran D. Bhattacharyya
# License: CC0

# import relevant libraries
import pandas as pd
import re
import glob
import csv

# grab all files with links to bills
billInfoFiles = glob.glob('D:/Projects/CongressionalDataProject/Data/*_billInfo.pkl')
billCosponFiles = glob.glob('D:/Projects/CongressionalDataProject/Data/*_billCosponNames.csv')

# create lists to store all bill data
billNumber = list()
billName = list()
billDate = list()
billStatus = list()
billSponsor = list()
billNumOfCosponsors = list()
billPartisanScore = list()

# iterate through each file name of bill data for a representative and cosponsor names
for i in range(0,len(billInfoFiles)):
    thisBillInfoFile = billInfoFiles[i] # grab file names
    thisBillCosponFile = billCosponFiles[i]

    # load in files
    billData = pd.read_pickle(thisBillInfoFile)
    with open(thisBillCosponFile, 'rb') as f:
        reader = csv.reader(f)
        cosponNameList = list(reader)

    for j in range(0, len(billData)):
        billNumber.append(billData.MemberBillNumber[j].encode('ascii', 'ignore')) # save easy bill data
        billName.append(billData.MemberBillNames[j].encode('ascii', 'ignore'))
        billDate.append(billData.MemberBillIntro[j].encode('ascii', 'ignore'))
        billStatus.append(billData.MemberBillTrack[j].encode('ascii', 'ignore'))
        billSponsor.append(thisBillInfoFile[42:-13])
        billNumOfCosponsors.append(int(billData.MemberBillCosponsors[j]))

        # compute bill partisan Score
        thisBill_demCospons = 0
        thisBill_repCospons = 0
        thisBill_partisanScore = 0
        thisNameList = cosponNameList[j]
        for name in thisNameList:
            sqrBracketPos = name.find('[')
            partyInitial = name[sqrBracketPos + 1]
            if partyInitial == 'D':
                thisBill_demCospons = thisBill_demCospons + 1
            elif partyInitial == 'R':
                thisBill_repCospons = thisBill_repCospons + 1

        thisBill_partisanScore = float(thisBill_demCospons - thisBill_repCospons)/(float(billData.MemberBillCosponsors[j]) + 0.0001)
        billPartisanScore.append(thisBill_partisanScore)

# create dataframe from lists
allBillMasterData = pd.DataFrame(
    {'BillNumber': billNumber,
     'BillName': billName,
     'BillDate': billDate,
     'BillSponsor': billSponsor,
     'BillStatus': billStatus,
     'BillNumCosponsors': billNumOfCosponsors,
     'BillPartisanScore': billPartisanScore
    })

# save dataframe as pickle file
allBillMasterData.to_pickle('Data/allBillMasterData.pkl')
allBillMasterData.to_csv('Data/allBillMasterData.csv')
