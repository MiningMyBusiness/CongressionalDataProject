# Scrapes the summaries of all bills proposed since 2017 for all current members of congress
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

def getThisBillText(): # returns a list of copsonsors for this bill
    # grab page source and parse with BeautifulSoup
    page = browser.page_source
    soup = BeautifulSoup(page, 'html.parser')

    thisBillText = list() # create a list to store the cosponsors of this bill for this member

    # save all cosponsor names for this bill
    allPs= soup.find_all('p')
    for p in allPs:
        thisPText = p.get_text()
        thisBillText.append(thisPText.encode('ascii', 'ignore'))

    return thisBillText

# set wait time
waitTime = 10 # seconds

# grab all files with links to bills for each member
billInfoFiles = glob.glob('K:/Projects/CongressionalDataProject/Data/*_billInfo.pkl')

# set path from chromedriver and open browser
path_chromedriver = 'C:\Users\KiranB\Desktop\chromedriver'
browser = webdriver.Chrome(executable_path = path_chromedriver)

for thisFile in billInfoFiles: # for each file of bill data for each member
    if os.path.isfile(thisFile[:-13] + '_allBillText.csv') == False:
        billData = pd.read_pickle(thisFile) # read one file

        allBillText = list() # create a master list to store all texts for all bills for this member

        # for each link to each bill
        for i in range(0,len(billData)):

            billYear = int(billData.MemberBillIntro[i][-4:]) # get the year of introduction for the bill

            if billYear > 2016: # if the bill was introduced in 2016 or later

                webpage = billData.MemberBillLink[i] # grab the bill webpage

                browser.get(webpage) # go to the bill webpage

                time.sleep(waitTime) # wait for page to load

                thisBillText = getThisBillText() # get text for this bill

                allBillText.append(thisBillText) # add list to master list
            else:
                allBillText.append('na')

        # save master list with list of cosponsor names for each bill for each member
        fileName = thisFile[:-13] + '_allBillText.csv'
        with open(fileName, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(allBillText)

        f.close()
