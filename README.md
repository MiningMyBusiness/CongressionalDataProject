# Visualizing Congress: seeing the forest and the trees

This repo contains the code and data needed to make the visualizations found in the [Visualizing Congress: seeing the forest and the trees](https://plot.ly/~kdb6df/6/visualizing-congress-seeing-the-forest-and-the-trees/) project submitted to the Congressional Data Competition.

## Introduction

With thousands of pages of congressional data being made available online every year, the legistlative process is more open now than it has been before. However, The sheer volume of content makes it difficult to understand the activity of Congress as a whole and of members in particular. 

Through interactive visualizatons of data collected from [Congress.gov](https://www.congress.gov/), this project works towards that solution by exploring 
* the activities of Congress members
* the connections between Congress members
* and the connection of members to the legistlation. 

## Repo organization

### Code 
The files in the Code directory of the repo contain all revelant code files (python) used to generate plots found in the Figures directory. Furthermore, there is a subdirectory in the Code directory with all code files used to scrape data from the [Congress.gov](https://www.congress.gov/) webpage and extract keywords from bill summaries. 

### Figures
The html files in the Figures directory of the repo contain all relevant figures outputed by the code files in the Code Directory. 

### Data
The files in the Data directory are not human-readable and only readable with python code. These data are aggregations of raw data collected from scraping. These raw data files are available online and can be collected by running the webscraping code found in the repo under the Code directory. 
