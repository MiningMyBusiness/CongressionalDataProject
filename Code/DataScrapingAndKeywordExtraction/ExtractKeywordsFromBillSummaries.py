# Extracts keywords from bill summaries using TextRank
# Author: Kiran D. Bhattacharyya
# License: CC0

# import relevant libraries
import pandas as pd
import re
import glob
import csv
import nltk
import numpy as np

def getKeywords(fullSummary):
    summaryKeywords = list() # create list to store keywords
    tokenSummary = nltk.word_tokenize(fullSummary) # tokenize summary
    summary_pos = nltk.pos_tag(tokenSummary) # tag parts of speech

    # syntactic filtering
    summary_synFilt = list() # create list to store syntactically filtered summary
    for word in summary_pos: # go through each word and pick out adjective and nouns
        if 'JJ' in word[1] or 'NN' in word[1]:
            if word[0] not in summary_synFilt: # if the work isn't already in the list, then add
                summary_synFilt.append(word[0])

    # creating connectivity matrix
    if len(summary_synFilt) > 100: # limit the number of words so the program doesn't crash
        summary_synFilt = summary_synFilt[0:100]
    if len(summary_synFilt) < 11:
        summaryKeywords.append(summary_synFilt)
    else:
        myWordDist = 2 # distance between words to make a connection
        connMat = np.zeros((len(summary_synFilt), len(summary_synFilt))) # create connectivity matrix
        for kk in range(0,len(summary_synFilt)): # for each word in the syntactic filtered list
            word = summary_synFilt[kk]
            indices_thisWord = np.array([k for k, x in enumerate(tokenSummary) if x == word]) # find indices of occurance for this word
            for ll in range(0,len(summary_synFilt)): # for the other words in the list
                if kk != ll: # if they are not the same word
                    otherWord = summary_synFilt[ll] # grab the word
                    indices_otherWord = np.array([k for k, x in enumerate(tokenSummary) if x == otherWord]) # find indicies of occurance for the other word

                    for index in indices_thisWord: # for each index of this word
                        thisIndexDiff = np.abs(indices_otherWord - index) # find distance between that index and all indicies of the other word
                        if np.min(thisIndexDiff) < (myWordDist + 1): # if the minimum distance is less than threshold
                            connMat[kk,ll] = 1 # create connection between words

        # iterate on text rank algorithm
        dampFactor = 0.85 # damping factor
        numOfIters = 20 # number of iterations on the word score
        numOfKeywords = 10 # number of keywords to grab
        wordScore = np.ones(len(summary_synFilt)) # create variable to store word scores
        for myIter in range(0,numOfIters): # loop for each iteration
            for kk in range(0,len(summary_synFilt)): # for each word
                thisWordConn = connMat[kk,:] # find all connections for this word
                otherWordIndx = [qq for qq, x in enumerate(thisWordConn) if x == 1] # find other words this word is connected to
                for index in otherWordIndx: # for each connected word
                    otherWordConn = connMat[index,:] # grab connections to this other word
                    wordScore[kk] = ((1/np.sum(otherWordConn))*wordScore[index]) + wordScore[kk]
                wordScore[kk] = (1 - dampFactor) + (dampFactor*wordScore[kk])

        sort_score = np.argsort(wordScore[::-1]) # sort scores in descending order
        for getKeywords in range(0,numOfKeywords):
            summaryKeywords.append(summary_synFilt[sort_score[getKeywords]])

    return summaryKeywords

# grab all files with links to bills
billInfoFiles = glob.glob('D:/Projects/CongressionalDataProject/Data/*_billInfo.pkl')
billSummaryFiles = glob.glob('D:/Projects/CongressionalDataProject/Data/*_allBillText.csv')

# create lists to store all bill data
billNumber = list()
billName = list()
billDate = list()
billSponsor = list()
billKeywords = list()

# iterate through each file name of bill data for a representative and cosponsor names
for i in range(0,len(billInfoFiles)):
    print i
    thisBillInfoFile = billInfoFiles[i] # grab file names
    thisSummaryFile = billSummaryFiles[i]

    # load in files for member bill data and bill summaries
    billData = pd.read_pickle(thisBillInfoFile)
    with open(thisSummaryFile, 'rb') as f:
        reader = csv.reader(f)
        billSummaries = list(reader)

    iterCount = 0
    matchIter = 0

    # go through each bill for this member
    for j in range(0, len(billData)):
        thisNumber = billData.MemberBillNumber[j].encode('ascii', 'ignore')
        thisName = billData.MemberBillNames[j].encode('ascii', 'ignore')
        thisDate = billData.MemberBillIntro[j].encode('ascii', 'ignore')
        thisSponsor = thisBillInfoFile[42:-13].encode('ascii', 'ignore')
        thisBillSummary = 'nothing' # assign a dummy value to this bill summary
        if int(thisDate[-4:]) > 2016: # if this bill was proposed in 2017 or after
            print j
            for summary in billSummaries: # check all bill summaries to find if one has this bills name
                for bit in summary: # for each bit in the summary
                    if thisName in bit: # check if any bits has the name of this bill
                         thisBillSummary = summary # if so, save the summary
            if len(thisBillSummary) > 1: # if dummy value has been reassigned
                sumStartIndx = 0 # create variables to start start and end index of the bill summary
                sumEndIndx = 0
                for k in range(0,len(thisBillSummary)): # look through list with summary
                    if thisName in thisBillSummary[k]:
                        sumStartIndx = k + 1 # and find start and stop indices for summary
                    if '\nEmail\n\n' in thisBillSummary[k]:
                        sumEndIndx = k - 1
                grabSummary = thisBillSummary[sumStartIndx:sumEndIndx] # grab summary
                fullSummary = ' '.join(grabSummary) # combine multiple lists into one summary list
                fullSummary = fullSummary.lower()

                # Start Keyword Extraction
                # preprocessing
                summaryKeywords = list()
                if fullSummary: # if the summary exists
                    summaryKeywords = getKeywords(fullSummary)

                billNumber.append(thisNumber)
                billName.append(thisName)
                billDate.append(thisDate)
                billSponsor.append(thisSponsor)
                billKeywords.append(summaryKeywords)

# create dataframe from lists
billKeywords2017 = pd.DataFrame(
    {'BillNumber': billNumber,
     'BillName': billName,
     'BillDate': billDate,
     'BillSponsor': billSponsor,
     'BillKeywords': billKeywords
    })

# save dataframe as pickle file
billKeywords2017.to_pickle('Data/billKeywords2017.pkl')
billKeywords2017.to_csv('Data/billKeywords2017.csv')











            # iterCount = iterCount + 1
            # billNumber.append(thisNumber.encode('ascii', 'ignore')) # save easy bill data
            # billName.append(thisName.encode('ascii', 'ignore'))
            # billDate.append(thisDate.encode('ascii', 'ignore'))
            # oneSummary = billSummary[j][4] # grab bill summary
            # print thisName
            # print oneSummary
