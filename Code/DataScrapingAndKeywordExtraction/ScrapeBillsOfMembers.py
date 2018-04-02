# Scrapes all relevant info on bills sponsored by current members
# Author: Kiran D. Bhattacharyya
# License: CC0

# import libraries
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

# load data
memberData = pd.read_pickle('Data/memberData.pkl')

# set wait time
waitTime = 10 # seconds

def getMemberBillInfo():
    # grab page source and parse with BeautifulSoup
    page = browser.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # create lists to store values
    memberBillNames = list()
    memberBillIntro = list()
    memberBillCospon = list()
    memberBillTrack = list()
    memberBillLink = list()
    memberBillNumber = list()
    memberParty = "N/A"

    # grab bill name, date of introduction, number of sponsors, and bill status
    allSpans = soup.find_all('span')
    for span in allSpans:
          thisClass = span.get('class')
          if thisClass:
              if 'result-heading' in thisClass:
                  thisA = span.find_all('a')
                  thisLink = thisA[0].get('href')
                  if thisLink:
                      if 'https://www.congress.gov/bill/' in thisLink:
                          if 'cosponsors?' not in thisLink:
                              if 'all-actions?' not in thisLink:
                                  if 'text?' not in thisLink:
                                      billLink = thisLink
                                      memberBillLink.append(billLink) # link to bill profile
                                      billNumber = thisA[0].get_text()
                                      memberBillNumber.append(billNumber) # bill number
              if 'result-title' in thisClass:
                  billName = span.get_text() # get bill name
                  memberBillNames.append(billName)
              if 'result-item' in thisClass:
                  timeAndCosp = span.get_text()
                  introIndx = timeAndCosp.find('(Introduced')
                  if introIndx > -1:
                      billIntroduced = timeAndCosp[(introIndx+12):(introIndx + 22)]
                      memberBillIntro.append(billIntroduced) # get date of bill introduction
                      cosponIndx = timeAndCosp.find('Cosponsors:')
                      cosponText = timeAndCosp[cosponIndx:]
                      cosponText = cosponText.strip()
                      numOfCospons = cosponText[13:-1] # number of cosponsors
                      memberBillCospon.append(numOfCospons)
              if 'result-tracker' in thisClass:
                  trackText = span.get_text()
                  billStatusStart = trackText.find('This bill has the status')
                  billStatusEnd = trackText.find('Here are the steps for')
                  billTracker = trackText[(billStatusStart + 25):billStatusEnd]
                  memberBillTrack.append(billTracker) # bill status

    # remove repeat results
    MemberBillNames = list() # create lists to store values
    MemberBillIntro = list()
    MemberBillCospon = list()
    MemberBillTrack = list()
    MemberBillLink = list()
    MemberBillNumber = list()

    oldName = 'nothing'
    for x in range(0,len(memberBillNames)):
        newName = memberBillNames[x]
        if oldName != newName:
            MemberBillNames.append(memberBillNames[x])
            MemberBillIntro.append(memberBillIntro[x])
            MemberBillCospon.append(memberBillCospon[x])
            MemberBillTrack.append(memberBillTrack[x])
            MemberBillLink.append(memberBillLink[x])
            MemberBillNumber.append(memberBillNumber[x])
        oldName = newName

    # get party affiliation
    allTrs = soup.find_all('tr')
    if allTrs:
        trText = allTrs[-1].get_text()
        partyIndx = trText.find('Party')
        memberParty = trText[(partyIndx + 6):-1]

    # return all values
    return MemberBillNames, MemberBillIntro, MemberBillCospon, MemberBillTrack, MemberBillLink, MemberBillNumber, memberParty

# set path from chromedriver and open browser
path_chromedriver = 'C:\Users\Kiran B\Desktop\chromedriver'
browser = webdriver.Chrome(executable_path = path_chromedriver)

allMemberParty = list()

# open pages in a loop
startIndx = 0 # start index for loop
stopIndx = len(memberData.SponsoredLegislationLink) # send index for looping
for x in range(startIndx, stopIndx):
    browser.get(memberData.SponsoredLegislationLink[x])
    time.sleep(waitTime)
    memberBillNames, memberBillIntro, memberBillCospon, memberBillTrack, memberBillLink, memberBillNumber, memberParty = getMemberBillInfo()
    memberNameSqueeze = memberData.MemberName[x].replace(" ", "")
    memberNameSqueeze = re.sub(r'[^\w]', '', memberNameSqueeze)
    fileName = 'Data/' + memberNameSqueeze + '_billInfo.pkl'
    memberBillInfo = pd.DataFrame(
        {'MemberBillNames': memberBillNames,
         'MemberBillIntro': memberBillIntro,
         'MemberBillCosponsors': memberBillCospon,
         'MemberBillTrack': memberBillTrack,
         'MemberBillLink': memberBillLink,
         'MemberBillNumber': memberBillNumber
        })
    allMemberParty.append(memberParty)

    # save into DataFrame
    memberBillInfo.to_pickle(fileName)

### REMEMBER TO SAVE THE MEMBER PARTY INTO THE MEMBERDATA.PKL FILE!!!!!
