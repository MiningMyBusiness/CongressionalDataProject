# Info on data scraping and keyword extraction files 

This folder contains all code files used to scrape, aggregate and analyze data to create processed data files that were used for visualizations. 

## Details on each file 

### ScrapeCongressMemberGenInfo.py
This code scrapes the Congress.gov webpage for all current members and associated member info. This is the first scraper that has to be run. WARNING: This scraper will take a few minutes to run 

### ScrapeBillsOfMembers.py
This code scrapes the names and webpages of all sponsored bills from all current congress members. This is the second scraper that has to be run. WARNING: This scraper will take hours to run. 

### ScrapeBillCosponsors.py
This code scrapes the names of all consponsors for all sponsored bills from all current members. WARNING: This code will take days to run. 

### ScrapeBillSummaries.py
The code scrapes the summaries of all bills introduced since 2017 for all current members of congress. WARNING: This code will take days to run. 

### CreateMasterBillDataset.py
This code aggregates all collected bill data for all current congress members into one master file. 

### CosponsorNetworkAnalysis.py
This code creates the sponsor-to-cosponsor connectivity matrices and analyzes the networks with PageRank to identify important nodes in the network. 

### ExtractKeywordsFromBillSummaries.py
This code extracts keywords from the scraped bill summaries and saves them to a master keywords database. 

WARNING: Please be aware that scraping code, network analysis code, and keyword extraction code can take a long time to run. 
