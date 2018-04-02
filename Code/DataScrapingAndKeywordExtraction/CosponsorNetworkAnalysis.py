# Creates and analyses sponsor-cosponsor connectivity matrix for members
# Author: Kiran D. Bhattacharyya
# License: CC0

# import relevant libraries
import pandas as pd
import re
import glob
import csv
import numpy as np

# grab all files with links to bills
memberData = pd.read_pickle('Data/memberData.pkl')
billCosponFiles = glob.glob('D:/Projects/CongressionalDataProject/Data/*_billCosponNames.csv')

# create connectivity matrix
repIndx = [k for k, x in enumerate(memberData.MemberName) if 'Representative' in x] # find index of representatives
senIndx = [k for k, x in enumerate(memberData.MemberName) if 'Senator' in x] # find index of senators
connMat_rep = np.zeros((len(repIndx), len(repIndx))) # create connectivity matrices
repName = list()
repFullName = list()
repParty = list()
connMat_sen = np.zeros((len(senIndx), len(senIndx)))
senName = list()
senFullName = list()
senParty = list()

# creat list of represenatative with turncated names
for i in range(0,len(repIndx)):
    memberNameSqueeze = memberData.MemberName[repIndx[i]].replace(" ", "") # make name into file name
    memberNameSqueeze = re.sub(r'[^\w]', '', memberNameSqueeze)
    repName.append(memberNameSqueeze)
    repFullName.append(memberData.MemberName[repIndx[i]])
    repParty.append(memberData.MemberParty[repIndx[i]])

# create list of senators with turncated names
for i in range(0,len(senIndx)):
    memberNameSqueeze = memberData.MemberName[senIndx[i]].replace(" ", "") # make name into file name
    memberNameSqueeze = re.sub(r'[^\w]', '', memberNameSqueeze)
    senName.append(memberNameSqueeze)
    senFullName.append(memberData.MemberName[senIndx[i]])
    senParty.append(memberData.MemberParty[senIndx[i]])

# populate connectivity matrix of representatives
for i in range(0,len(repName)):
    name = repName[i] # get rep name
    memberAllCospon = list() # create list to call in
    for file in billCosponFiles: # for each file of cospon list
        if file[42:-20] in name: # see if name is in the file name
            with open(file, 'rb') as f:
                reader = csv.reader(f)
                memberAllCospon = list(reader)

    for listCospon in memberAllCospon: # for each list of cosponsors
        for cospon in listCospon: # for each cosponsor in the list
            commaIndx = cospon.find(',')
            lastName = cospon[5:commaIndx] # grab the last name
            bracketIndx = cospon[(commaIndx+2):].find(' ')
            firstName = cospon[(commaIndx+2):(commaIndx+2+bracketIndx)] # grab last name
            cosponNameIndx = [k for k, x in enumerate(repName) if lastName in x and firstName in x]
            connMat_rep[i,cosponNameIndx] = connMat_rep[i,cosponNameIndx] + 1

# populate connectivity matrix of senators
for i in range(0,len(senName)):
    name = senName[i] # get senator name
    memberAllCospon = list() # create list to call in
    for file in billCosponFiles: # for each file of cospon list
        if file[42:-20] in name: # see if name is in the file name
            with open(file, 'rb') as f:
                reader = csv.reader(f)
                memberAllCospon = list(reader)

    for listCospon in memberAllCospon: # for each list of cosponsors
        for cospon in listCospon: # for each cosponsor in the list
            commaIndx = cospon.find(',')
            lastName = cospon[5:commaIndx] # grab the last name
            bracketIndx = cospon[(commaIndx+2):].find(' ')
            firstName = cospon[(commaIndx+2):(commaIndx+2+bracketIndx)] # grab last name
            cosponNameIndx = [k for k, x in enumerate(senName) if lastName in x and firstName in x]
            connMat_sen[i,cosponNameIndx] = connMat_sen[i,cosponNameIndx] + 1

# save connectivity matrix for representatives and
np.save('Data/RepresentativeConnMat.npy', connMat_rep)
np.save('Data/SenatorConnMat.npy', connMat_sen)

# Run page rank on each connectivity matrix

# for representatives
dampFactor = 0.85 # damping factor
numOfIters = 30 # number of iterations on the member score
repScore = np.ones(len(repName)) # initialize member scores
for myIter in range(0,numOfIters):
    for i in range(0,len(repName)): # for each member
        thisRepIn = connMat_rep[:,i] # grab all incoming connections
        otherRepIndx = [qq for qq, x in enumerate(thisRepIn) if x > 0] # get index of other members this member is connected to
        for index in otherRepIndx:
            otherRepOut = connMat_rep[index,:]
            repScore[i] = ((connMat_rep[index,i]/np.sum(otherRepOut))*repScore[index]) + repScore[i]
        repScore[i] = (1 - dampFactor) + (dampFactor*repScore[i])

# for senators
senScore = np.ones(len(senName)) # initialize member scores
for myIter in range(0,numOfIters):
    for i in range(0,len(senName)): # for each member
        thisSenIn = connMat_sen[:,i] # grab all incoming connections
        otherSenIndx = [qq for qq, x in enumerate(thisSenIn) if x > 0] # get index of other members this member is connected to
        for index in otherSenIndx:
            otherSenOut = connMat_sen[index,:]
            senScore[i] = ((connMat_sen[index,i]/np.sum(otherSenOut))*senScore[index]) + senScore[i]
        senScore[i] = (1 - dampFactor) + (dampFactor*senScore[i])

# create dataframe from lists
repCosponNetwork = pd.DataFrame(
    {'MemberName': repName,
     'MemberFullName': repFullName,
     'MemberParty': repParty,
     'MemberNetworkScore': repScore
    })

senCosponNetwork = pd.DataFrame(
    {'MemberName': senName,
     'MemberFullName': senFullName,
     'MemberParty': senParty,
     'MemberNetworkScore': senScore
    })

# save files
repCosponNetwork.to_pickle('Data/RepresentativeNetworkScore.pkl')
repCosponNetwork.to_csv('Data/RepresentativeNetworkScore.csv')

senCosponNetwork.to_pickle('Data/SenatorNetworkScore.pkl')
senCosponNetwork.to_csv('Data/SenatorNetworkScore.csv')





#
#
#
#
#
