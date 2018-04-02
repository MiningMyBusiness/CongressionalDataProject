# Scrapes cosponsors for all sponsored bills of current congress members
# Author: Kiran D. Bhattacharyya
# License: CC0

# import libraries
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import glob
import csv
import os.path

def getThisBillCospon(): # returns a list of copsonsors for this bill
    # grab page source and parse with BeautifulSoup
    page = browser.page_source
    soup = BeautifulSoup(page, 'html.parser')

    thisBillCospon = list() # create a list to store the cosponsors of this bill for this member

    # save all cosponsor names for this bill
    allTds = soup.find_all('td')
    for td in allTds:
        thisClass = td.get('class')
        if thisClass:
            if 'actions' in thisClass:
                thisSponName = td.get_text()
                thisSponName = thisSponName.strip()
                thisBillCospon.append(thisSponName)

    return thisBillCospon

# set wait time
waitTime = 10 # seconds

# grab all files with links to bills for each member
billInfoFiles = glob.glob('K:/Projects/CongressionalDataProject/Data/*_billInfo.pkl')

# set path from chromedriver and open browser
path_chromedriver = 'C:\Users\KiranB\Desktop\chromedriver'
browser = webdriver.Chrome(executable_path = path_chromedriver)

for thisFile in billInfoFiles: # for each file of bill data for each member
    if os.path.isfile(thisFile[:-13] + '_billCosponNames.csv') == False:
        billData = pd.read_pickle(thisFile) # read one file

        allBillCospon = list() # create a master list to store all cosponsors for all bills for this member

        # for each link to each bill
        for webpage in billData.MemberBillLink:
            thisWebpage = webpage + '/cosponsors' # get a webpage from the billData dataframe

            browser.get(thisWebpage) # go to the bill webpage

            time.sleep(waitTime) # wait for page to load

            thisBillCospon = getThisBillCospon() # get list of cosponsors for this bill

            allBillCospon.append(thisBillCospon) # add list to master list

        # save master list with list of cosponsor names for each bill for each member
        fileName = thisFile[:-13] + '_billCosponNames.csv'
        with open(fileName, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(allBillCospon)
