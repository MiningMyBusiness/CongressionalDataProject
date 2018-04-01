# Makes member-keyword network in house and senate
# Author: Kiran D. Bhattacharyya
# Conception: Kiran D. Bhattacharyya and Sara Milkes
# License: CC0

# import relevant libraries
import pandas as pd
import re
import glob
import csv
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx

# read in relevant files
billKeywords2017 = pd.read_pickle('../Data/billKeywords2017.pkl')
allBillData = pd.read_pickle('../Data/allBillMasterData.pkl')

# create lists to store data about selected congress members
house_dem_name = 'RepresentativeJamesPMcGovern'
house_dem_keywords = list()
house_rep_name = 'RepresentativeTrentFranks'
house_rep_keywords = list()
house_mid_name = 'RepresentativeChristopherHSmith'
house_mid_keywords = list()

sen_dem_name = 'SenatorPattyMurray'
sen_dem_keywords = list()
sen_rep_name = 'SenatorRoyBlunt'
sen_rep_keywords = list()
sen_mid_name = 'SenatorSusanMCollins'
sen_mid_keywords = list()

# find index of relevant data about congress members in data files
house_dem_keyIndx = [k for k, x in enumerate(billKeywords2017.BillSponsor) if house_dem_name in x]
sen_dem_keyIndx = [k for k, x in enumerate(billKeywords2017.BillSponsor) if sen_dem_name in x]
house_rep_keyIndx = [k for k, x in enumerate(billKeywords2017.BillSponsor) if house_rep_name in x]
sen_rep_keyIndx = [k for k, x in enumerate(billKeywords2017.BillSponsor) if sen_rep_name in x]
house_mid_keyIndx = [k for k, x in enumerate(billKeywords2017.BillSponsor) if house_mid_name in x]
sen_mid_keyIndx = [k for k, x in enumerate(billKeywords2017.BillSponsor) if sen_mid_name in x]

# create lists to store keywords for each member
house_dem_keywords = list()
sen_dem_keywords = list()
house_rep_keywords = list()
sen_rep_keywords = list()
house_mid_keywords = list()
sen_mid_keywords = list()

# for each member populate list of keywords from master keyword data
for index in house_dem_keyIndx:
    theseKeywords = billKeywords2017.BillKeywords[index]
    if theseKeywords:
        if len(theseKeywords[0][0]) == 1:
            for word in theseKeywords:
                house_dem_keywords.append(word)
        if len(theseKeywords[0][0]) > 1:
            for sublist in theseKeywords:
                for word in sublist:
                    house_dem_keywords.append(word)

for index in house_rep_keyIndx:
    theseKeywords = billKeywords2017.BillKeywords[index]
    if theseKeywords:
        if len(theseKeywords[0][0]) == 1:
            for word in theseKeywords:
                house_rep_keywords.append(word)
        if len(theseKeywords[0][0]) > 1:
            for sublist in theseKeywords:
                for word in sublist:
                    house_rep_keywords.append(word)

for index in house_mid_keyIndx:
    theseKeywords = billKeywords2017.BillKeywords[index]
    if theseKeywords:
        if len(theseKeywords[0][0]) == 1:
            for word in theseKeywords:
                house_mid_keywords.append(word)
        if len(theseKeywords[0][0]) > 1:
            for sublist in theseKeywords:
                for word in sublist:
                    house_mid_keywords.append(word)

for index in sen_dem_keyIndx:
    theseKeywords = billKeywords2017.BillKeywords[index]
    if theseKeywords:
        if len(theseKeywords[0][0]) == 1:
            for word in theseKeywords:
                sen_dem_keywords.append(word)
        if len(theseKeywords[0][0]) > 1:
            for sublist in theseKeywords:
                for word in sublist:
                    sen_dem_keywords.append(word)

for index in sen_rep_keyIndx:
    theseKeywords = billKeywords2017.BillKeywords[index]
    if theseKeywords:
        if len(theseKeywords[0][0]) == 1:
            for word in theseKeywords:
                sen_rep_keywords.append(word)
        if len(theseKeywords[0][0]) > 1:
            for sublist in theseKeywords:
                for word in sublist:
                    sen_rep_keywords.append(word)

for index in sen_mid_keyIndx:
    theseKeywords = billKeywords2017.BillKeywords[index]
    if theseKeywords:
        if len(theseKeywords[0][0]) == 1:
            for word in theseKeywords:
                sen_mid_keywords.append(word)
        if len(theseKeywords[0][0]) > 1:
            for sublist in theseKeywords:
                for word in sublist:
                    sen_mid_keywords.append(word)

# collapse keyword list
masterKeywordList = [house_dem_keywords, house_rep_keywords, house_mid_keywords,
                    sen_dem_keywords, sen_rep_keywords, sen_mid_keywords]
flat_keywordList = [item for sublist in masterKeywordList for item in sublist]
uniqWords_full = list(set(flat_keywordList))

# find unique keywords by excluding non-sensical stop words
myStopWords = list()
myStopWords.append('fy2022')
myStopWords.append('orhigh-risk')
myStopWords.append('fy2016')
myStopWords.append('%')
myStopWords.append('fy2018-fy2019')
myStopWords.append('i')
myStopWords.append('60-day')
myStopWords.append('losaps')
myStopWords.append('todrugs')
uniqWords = list()
for word in uniqWords_full:
    if word not in myStopWords:
        if len(word) > 4:
            uniqWords.append(word)

# create connectivity matrix between members and keywords
numOfWords = len(uniqWords)
numOfPeople = 6
totalNodes = numOfPeople + numOfWords
connMat = np.zeros((totalNodes, totalNodes))
for i in range(6,totalNodes):
    thisWord = uniqWords[i-numOfPeople]
    if thisWord in house_dem_keywords:
        connMat[0,i] = 1
        connMat[i,0] = 1
    if thisWord in house_rep_keywords:
        connMat[1,i] = 1
        connMat[i,1] = 1
    if thisWord in house_mid_keywords:
        connMat[2,i] = 1
        connMat[i,2] = 1
    if thisWord in sen_dem_keywords:
        connMat[3,i] = 1
        connMat[i,3] = 1
    if thisWord in sen_rep_keywords:
        connMat[4,i] = 1
        connMat[i,4] = 1
    if thisWord in sen_mid_keywords:
        connMat[5,i] = 1
        connMat[i,5] = 1

###########################################################
# create netowrk from connectivity matrix for House of Reps
G = nx.from_numpy_matrix(connMat)

# get node positions
pos = nx.spring_layout(G, dim=3)

# get x and y coordinates of nodes
Xn=[pos[k][0] for k in range(0,G.number_of_nodes())]# x-coordinates of nodes
Yn=[pos[k][1] for k in range(0,G.number_of_nodes())]# y-coordinates
Zn=[pos[k][2] for k in range(0,G.number_of_nodes())]# y-coordinates

# populate node edges
Edges = G.edges()
Xe=[]
Ye=[]
Ze=[]
for e in Edges:
    Xe+=[pos[e[0]][0],pos[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[pos[e[0]][1],pos[e[1]][1], None]
    Ze+=[pos[e[0]][2],pos[e[1]][2], None]

# add trace for edges
edge_trace = go.Scatter3d(
    x=Xe,
    y=Ye,
    z=Ze,
    line=go.Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

# add trace for members in the house
house_trace = go.Scatter3d(
    x=Xn[0:3],
    y=Yn[0:3],
    z=Zn[0:3],
    mode='markers',
    name='Member of the House',
    text=['Name: Representative James P. McGovern', 'Name: Representative Trent Franks',
            'Name: Represenatative Christopher H. Smith'],
    hoverinfo='text',
    marker=dict(
        symbol='dot',
        size=20,
        color=['rgb(56, 94, 244)','rgb(247, 59, 59)','rgb(247, 59, 59)'],
        # sizeref=2.*max(uniqWordNumBills)/(10.**2),
        # sizemin=3
    )
)

# add trace for members in the senate
sen_trace = go.Scatter3d(
    x=Xn[3:6],
    y=Yn[3:6],
    z=Zn[3:6],
    mode='markers',
    name='Member of the Senate',
    text=['Name: Senator Patty Murray', 'Name: Senator Roy Blunt', 'Name: Senator Susan M. Collins'],
    hoverinfo='text',
    marker=dict(
        symbol='dot',
        size=20,
        color=['rgb(56, 94, 244)','rgb(247, 59, 59)','rgb(247, 59, 59)'],
        # sizeref=2.*max(uniqWordNumBills)/(10.**2),
        # sizemin=3
    )
)

# add trace for keywords
keyword_trace = go.Scatter3d(
    x=Xn[6:],
    y=Yn[6:],
    z=Zn[6:],
    mode='markers',
    name='Keywords',
    text=uniqWords,
    hoverinfo='text',
    marker=dict(
        symbol='dot',
        size=10,
        color='rgb(166, 8, 206)',
        # sizeref=2.*max(uniqWordNumBills)/(10.**2),
        # sizemin=3
    )
)

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

data = [edge_trace, house_trace, sen_trace, keyword_trace]

# create layout for plotly
layout = go.Layout(
         title="Member-Keyword Network from bills proposed since 2017",
         width=1000,
         height=1000,
         showlegend=False,
         scene= go.Scene(
         xaxis= go.XAxis(axis),
         yaxis= go.YAxis(axis),
         zaxis= go.ZAxis(axis),
        ),
     margin= go.Margin(
        t=100
    ),
         hovermode='closest'
      )

# plot figures
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='../Figures/KeywordMemberNetwork_2.html')




##
##
##
##
