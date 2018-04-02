# Scrapes the name, profile page, and other relevant info for current congress members 
# Author: Kiran D. Bhattacharyya
# License: CC0

# import libraries
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import pandas as pd

waitTime = 10 # wait time in seconds for page to load

## Function definitions
# functions checks to see if a certain class name element exists on the webpage
def check_exists_by_class_name(name):
    try:
        browser.find_element_by_class_name(name)
    except NoSuchElementException:
        return False
    return True

# total number of members
def getTotalNumberOfMembers():
    # pull page source and parse
    page = browser.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # get the total number of results
    allSpan = soup.find_all('span')
    for span in allSpan:
        thisText = span.get_text()
        if ' of ' in thisText:
            shortText = thisText.strip()
            numberOfMembers = shortText[-3:]
    return int(numberOfMembers)


# function pulls links to congress members profile pages
def getMemberLinks():
    # pull page source and parse
    page = browser.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # get the elements of interest
    allAs = soup.find_all('a')
    allLinks = list();
    for link in allAs:
        thisLink = link.get('href')
        allLinks.append(thisLink)

    # extract links of interest to congress member pages
    linksOfMembers = list()
    oldLink = 'nothing'
    for link in allLinks:
        if link != oldLink:
            if 'https://www.congress.gov/member/' in link:
                linksOfMembers.append(link)
        oldLink = link
    return linksOfMembers

def getMemberDetails():
    # pull page source and parse
    page = browser.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # get congress person name, state, district, and residency
    allTitleLinks = soup.head.find_all('link')
    thisName = allTitleLinks[1]['title'] # get name
    firstTable = soup.table
    allTds = firstTable.find_all('td')
    thisState = allTds[0].get_text() # get state
    thisDistrict = allTds[1].get_text().strip()
    thisResidency = allTds[2].get_text().strip() # get getResidency

    # get number of sponsored and cosponsored legislation
    allSpans = soup.find_all('span')
    sponsCountNumber = ''
    cosponCountNumber = ''
    for span in allSpans:
        thisText = span.get('id')
        if thisText:
            if 'Sponsored_Legislationcount' in thisText:
                countText = span.get_text()
                countText = countText.replace(',','')
                sponsCountNumber = int(countText[1:-1])
            if 'Cosponsored_Legislationcount' in thisText:
                countText = span.get_text()
                countText = countText.replace(',','')
                cosponCountNumber = int(countText[1:-1])

    # grab link for sponsored legislation page
    allAs = soup.find_all('a')
    thisSponsLink = ''
    for thisA in allAs:
        thisId = thisA.get('id')
        if thisId:
            if 'facetItemsponsorshipSponsored_Legislation' in thisId:
                thisSponsLink = thisA.get('href')

    # return all values
    return thisName, thisState, thisDistrict, thisResidency, sponsCountNumber, cosponCountNumber, thisSponsLink


## Main code
path_chromedriver = 'C:\Users\KiranB\Desktop\chromedriver'
browser = webdriver.Chrome(executable_path = path_chromedriver)

# specify webpage and open
myWebpage = 'https://www.congress.gov/members?q=%7B%22congress%22%3A%22115%22%7D'
browser.get(myWebpage)

numberOfMembers = getTotalNumberOfMembers()
allMembers = getMemberLinks() # grab links of members
time.sleep(waitTime) # wait 10 seconds

# navigate to the next page of results
while len(allMembers) < numberOfMembers: # while our list does not have all the members
    elemExists_nextPage = check_exists_by_class_name("next") # check if there is a next page
    if elemExists_nextPage: # if there is a next page
        browser.find_element_by_class_name("next").click() # click on the button
        time.sleep(waitTime) # wait 10 seconds for page to load
        thisPageMembers = getMemberLinks() # grab links to pages of other members
        for link in thisPageMembers:
            allMembers.append(link)

# load page from congress person profile page
memberNames = list() # member names
memberState = list() # member state
memberDistrict = list() # member district
memberResidency = list() # member residency
memberSponsCount = list() # number of sponsored legislation
memberCosponCount = list() # number of cosponsored legislation
memberSponsLink = list() # link to sponsored legislation page
for link in allMembers:
    browser.get(link)
    time.sleep(waitTime)
    thisName, thisState, thisDistrict, thisResidency, sponsCountNumber, cosponCountNumber, thisSponsLink = getMemberDetails()
    thisSponsLink = 'https://www.congress.gov' + thisSponsLink
    memberNames.append(thisName)
    memberState.append(thisState)
    memberDistrict.append(thisDistrict)
    memberResidency.append(thisResidency)
    memberSponsCount.append(sponsCountNumber)
    memberCosponCount.append(cosponCountNumber)
    memberSponsLink.append(thisSponsLink)

# close browser
browser.close()

# put member data into a data frame
memberData = pd.DataFrame(
    {'MemberProfilePage': allMembers,
     'MemberName': memberNames,
     'MemberState': memberState,
     'MemberDistrict': memberDistrict,
     'MemberResidency': memberResidency,
     'NumOfSponseredLegislation': memberSponsCount,
     'NumOfCosponLegislation': memberCosponCount,
     'SponsoredLegislationLink': memberSponsLink
    })

# save DataFrame
memberData.to_pickle('memberData.pkl')
