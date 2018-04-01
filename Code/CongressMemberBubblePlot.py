# Makes bubble plots for congress members that show bills proposed, partisan score, and avg. num of cosponsors
# Author: Kiran D. Bhattacharyya
# License: CC0


# import relevant libraries
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import re
import numpy as np

# read in relevant data files
memberData = pd.read_pickle('../Data/memberData.pkl')
allBillData = pd.read_pickle('../Data/allBillMasterData.pkl')

# create lists to store and parse data
house_dem_name = list()
house_rep_name = list()
senate_dem_name = list()
senate_rep_name = list()
senate_ind_name = list()

house_rep_sponLeg = list()
house_dem_sponLeg = list()
senate_rep_sponLeg = list()
senate_dem_sponLeg = list()
senate_ind_sponLeg = list()

house_rep_avgCospon = list()
house_dem_avgCospon = list()
senate_rep_avgCospon = list()
senate_dem_avgCospon = list()
senate_ind_avgCospon = list()

house_rep_avgPartisan = list()
house_dem_avgPartisan = list()
senate_rep_avgPartisan = list()
senate_dem_avgPartisan = list()
senate_ind_avgPartisan = list()

# go through each member to find relevant data and sort into lists
for i in range(0,len(memberData)):
    thisName = memberData.MemberName[i]
    memberNameSqueeze = thisName.replace(" ", "")
    memberNameSqueeze = re.sub(r'[^\w]', '', memberNameSqueeze)

    thisMember_sponLeg = 0
    thisMember_avgCospon = 0
    thisMember_avgPartisan = 0

    allBillIndx = [k for k, x in enumerate(allBillData.BillSponsor) if memberNameSqueeze in x]

    if allBillIndx:
        for j in range(0,len(allBillIndx)):
            thisYear = int(allBillData.BillDate[allBillIndx[j]][-4:])
            if thisYear > 2016:
                thisMember_sponLeg = thisMember_sponLeg + 1
                thisMember_avgCospon = thisMember_avgCospon + allBillData.BillNumCosponsors[allBillIndx[j]]
                thisMember_avgPartisan = thisMember_avgPartisan + allBillData.BillPartisanScore[allBillIndx[j]]

        if thisMember_sponLeg > 0:
            thisMember_avgCospon = thisMember_avgCospon/thisMember_sponLeg
            thisMember_avgPartisan = thisMember_avgPartisan/thisMember_sponLeg

        if 'Representative' in thisName:
            if 'Demo' in memberData.MemberParty[i]:
                house_dem_sponLeg.append(thisMember_sponLeg)
                house_dem_avgCospon.append(thisMember_avgCospon)
                house_dem_name.append(thisName[15:])
                house_dem_avgPartisan.append(thisMember_avgPartisan)
            elif 'Repub' in memberData.MemberParty[i]:
                house_rep_sponLeg.append(thisMember_sponLeg)
                house_rep_avgCospon.append(thisMember_avgCospon)
                house_rep_name.append(thisName[15:])
                house_rep_avgPartisan.append(thisMember_avgPartisan)
        elif 'Senator' in thisName:
            if 'Demo' in memberData.MemberParty[i]:
                senate_dem_sponLeg.append(thisMember_sponLeg)
                senate_dem_avgCospon.append(thisMember_avgCospon)
                senate_dem_name.append(thisName[7:])
                senate_dem_avgPartisan.append(thisMember_avgPartisan)
            elif 'Repub' in memberData.MemberParty[i]:
                senate_rep_sponLeg.append(thisMember_sponLeg)
                senate_rep_avgCospon.append(thisMember_avgCospon)
                senate_rep_name.append(thisName[7:])
                senate_rep_avgPartisan.append(thisMember_avgPartisan)
            elif 'Ind' in memberData.MemberParty[i]:
                senate_ind_sponLeg.append(thisMember_sponLeg)
                senate_ind_avgCospon.append(thisMember_avgCospon)
                senate_ind_name.append(thisName[7:])
                senate_ind_avgPartisan.append(thisMember_avgPartisan)

####################### House bubble plot ###########################
# create lists of hover texts to plot with plotly
house_dem_hover_text = list()
house_dem_color = list()

for i in range(0,len(house_dem_name)):
    thisName = house_dem_name[i]
    thisParty = 'Democrat'
    thisNumOfSpon = str(house_dem_sponLeg[i])
    thisAvgCospon = str(house_dem_avgCospon[i])
    thisPartisan = str(house_dem_avgPartisan[i])
    house_dem_hover_text.append(('Name: ' + thisName + '<br>'+
                      'Party: ' + thisParty + '<br>'+
                      '# of Sponsored Bills: ' + thisNumOfSpon + '<br>'+
                      'Avg. # of Cosponsors: ' + thisAvgCospon + '<br>'+
                      'Avg. Partisan Score: ' + thisPartisan))
    house_dem_color.append('rgb(56, 94, 244)')

house_rep_hover_text = list()
house_rep_color = list()

for i in range(0,len(house_rep_name)):
    thisName = house_rep_name[i]
    thisParty = 'Republican'
    thisNumOfSpon = str(house_rep_sponLeg[i])
    thisAvgCospon = str(house_rep_avgCospon[i])
    thisPartisan = str(house_rep_avgPartisan[i])
    house_rep_hover_text.append(('Name: ' + thisName + '<br>'+
                      'Party: ' + thisParty + '<br>'+
                      '# of Sponsored Bills: ' + thisNumOfSpon + '<br>'+
                      'Avg. # of Cosponsors: ' + thisAvgCospon + '<br>'+
                      'Avg. Partisan Score: ' + thisPartisan))
    house_rep_color.append('rgb(247, 59, 59)')

# create traces in plotly for each party
trace0 = go.Scatter(
    x=house_dem_sponLeg + np.random.rand(len(house_dem_sponLeg)),
    y=house_dem_avgPartisan,
    mode='markers',
    name='Democrats',
    text=house_dem_hover_text,
    marker=dict(
        color=house_dem_color,
        size=house_dem_avgCospon,
        sizemode='area',
        sizeref=2.*max(house_rep_avgCospon)/(40.**2),
        sizemin=4
    )
)

trace1 = go.Scatter(
    x=house_rep_sponLeg + np.random.rand(len(house_rep_sponLeg)),
    y=house_rep_avgPartisan,
    mode='markers',
    name='Republicans',
    text=house_rep_hover_text,
    marker=dict(
        color=house_rep_color,
        size=house_rep_avgCospon,
        sizemode='area',
        sizeref=2.*max(house_rep_avgCospon)/(40.**2),
        sizemin=4
    )
)

data = [trace0, trace1]

# create plotly layout
layout = go.Layout(
    title='Productivity and Partisanship in the House',
    hovermode='closest',
    xaxis=dict(
        title='Number of sponsored bills since 2017',
        gridcolor='rgb(255, 255, 255)',
        range=[0, 70],
        zerolinewidth=1,
        ticklen=5,
        gridwidth=2,
    ),
    yaxis=dict(
        title='Average partisan score of sponsored bills',
        gridcolor='rgb(255, 255, 255)',
        range=[-1.1, 1.1],
        zerolinewidth=1,
        ticklen=0.2,
        gridwidth=0.1,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)

# plot using plotly
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='../Figures/HouseBubble.html')

####################### Senate bubble plot ###########################
# create lists with hover text
senate_dem_hover_text = list()
senate_dem_color = list()

for i in range(0,len(senate_dem_name)):
    thisName = senate_dem_name[i]
    thisParty = 'Democrat'
    thisNumOfSpon = str(senate_dem_sponLeg[i])
    thisAvgCospon = str(senate_dem_avgCospon[i])
    thisPartisan = str(senate_dem_avgPartisan[i])
    senate_dem_hover_text.append(('Name: ' + thisName + '<br>'+
                      'Party: ' + thisParty + '<br>'+
                      '# of Sponsored Bills: ' + thisNumOfSpon + '<br>'+
                      'Avg. # of Cosponsors: ' + thisAvgCospon + '<br>'+
                      'Avg. Partisan Score: ' + thisPartisan))
    senate_dem_color.append('rgb(56, 94, 244)')

senate_rep_hover_text = list()
senate_rep_color = list()

for i in range(0,len(senate_rep_name)):
    thisName = senate_rep_name[i]
    thisParty = 'Republican'
    thisNumOfSpon = str(senate_rep_sponLeg[i])
    thisAvgCospon = str(senate_rep_avgCospon[i])
    thisPartisan = str(senate_rep_avgPartisan[i])
    senate_rep_hover_text.append(('Name: ' + thisName + '<br>'+
                      'Party: ' + thisParty + '<br>'+
                      '# of Sponsored Bills: ' + thisNumOfSpon + '<br>'+
                      'Avg. # of Cosponsors: ' + thisAvgCospon + '<br>'+
                      'Avg. Partisan Score: ' + thisPartisan))
    senate_rep_color.append('rgb(247, 59, 59)')

# create traces for plotly
trace0 = go.Scatter(
    x=senate_dem_sponLeg + np.random.rand(len(senate_dem_sponLeg)),
    y=senate_dem_avgPartisan,
    mode='markers',
    name='Democrats',
    text=senate_dem_hover_text,
    marker=dict(
        color=senate_dem_color,
        size=senate_dem_avgCospon,
        sizemode='area',
        sizeref=2.*max(senate_rep_avgCospon)/(40.**2),
        sizemin=4
    )
)

trace1 = go.Scatter(
    x=senate_rep_sponLeg + np.random.rand(len(senate_rep_sponLeg)),
    y=senate_rep_avgPartisan,
    mode='markers',
    name='Republicans',
    text=senate_rep_hover_text,
    marker=dict(
        color=senate_rep_color,
        size=senate_rep_avgCospon,
        sizemode='area',
        sizeref=2.*max(senate_rep_avgCospon)/(40.**2),
        sizemin=4
    )
)

data = [trace0, trace1]

# create plotly layout
layout = go.Layout(
    title='Productivity and Partisanship in the Senate',
    hovermode='closest',
    xaxis=dict(
        title='Number of sponsored bills since 2017',
        gridcolor='rgb(255, 255, 255)',
        range=[0, 70],
        zerolinewidth=1,
        ticklen=5,
        gridwidth=2,
    ),
    yaxis=dict(
        title='Average partisan score of sponsored bills',
        gridcolor='rgb(255, 255, 255)',
        range=[-1.1, 1.1],
        zerolinewidth=1,
        ticklen=0.2,
        gridwidth=0.1,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)

# plot using plotly
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='../Figures/SenateBubble.html')
