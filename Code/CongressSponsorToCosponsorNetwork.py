# Makes sponsor-to-cosponsor network in house and senate
# Author: Kiran D. Bhattacharyya
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

# load in connectivity matrices
connMat_rep = np.load('../Data/RepresentativeConnMat.npy')
connMat_sen = np.load('../Data/SenatorConnMat.npy')

# load in meta data about connection matrices
repData = pd.read_pickle('../Data/RepresentativeNetworkScore.pkl')
senData = pd.read_pickle('../Data/SenatorNetworkScore.pkl')

# figure out total collaborations
collabMat_rep = np.zeros((len(connMat_rep), len(connMat_rep)))
billThresh = 15
for i in range(0,len(connMat_rep)):
    for j in range(0,len(connMat_rep)):
        totalAppearances = connMat_rep[i,j] + connMat_rep[j,i]
        if totalAppearances > billThresh:
            collabMat_rep[i,j] = 1
            collabMat_rep[j,i] = collabMat_rep[i,j]

# figure out total collaborations
collabMat_sen = np.zeros((len(connMat_sen), len(connMat_sen)))
billThresh = 15
for i in range(0,len(connMat_sen)):
    for j in range(0,len(connMat_sen)):
        totalAppearances = connMat_sen[i,j] + connMat_sen[j,i]
        if totalAppearances > billThresh:
            collabMat_sen[i,j] = 1
            collabMat_sen[j,i] = collabMat_sen[i,j]

###########################################################
# create network from connectivity matrix for House of Reps
G = nx.from_numpy_matrix(collabMat_rep)

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

# sort and add to lists x,y,z positions of nodes and hover text for plotly
Xn_demo = list()
Xn_repu = list()
Yn_demo = list()
Yn_repu = list()
Zn_demo = list()
Zn_repu = list()
adList = G.adjacency_list()
demo_hover_text = list()
repu_hover_text = list()
demo_numConns = list()
repu_numConns = list()
demo_color = list()
repu_color = list()
for i in range(0,len(repData)):
    thisName = repData.MemberFullName[i]
    thisParty = repData.MemberParty[i]
    thisNumConns = len(adList[i])
    if 'Dem' in thisParty:
        Xn_demo.append(Xn[i])
        Yn_demo.append(Yn[i])
        Zn_demo.append(Zn[i])
        demo_numConns.append(float(thisNumConns))
        demo_hover_text.append(('Name: ' + thisName + '<br>'+
                          'Party: ' + thisParty + '<br>'+
                          '# of Connections: ' + str(thisNumConns)))
        demo_color.append('rgb(56, 94, 244)')
    if 'Rep' in thisParty:
        Xn_repu.append(Xn[i])
        Yn_repu.append(Yn[i])
        Zn_repu.append(Zn[i])
        repu_numConns.append(float(thisNumConns))
        repu_hover_text.append(('Name: ' + thisName + '<br>'+
                          'Party: ' + thisParty + '<br>'+
                          '# of Connections: ' + str(thisNumConns)))
        repu_color.append('rgb(247, 59, 59)')

# create traces for plotly
node_trace_demo = go.Scatter3d(
    x=Xn_demo,
    y=Yn_demo,
    z=Zn_demo,
    mode='markers',
    name='Democrats',
    text=demo_hover_text,
    hoverinfo='text',
    marker=dict(
        symbol='dot',
        color=demo_color,
        size=demo_numConns,
        sizeref=2.*max(demo_numConns)/(10.**2),
        sizemin=3
    )
)

node_trace_repu = go.Scatter3d(
    x=Xn_repu,
    y=Yn_repu,
    z=Zn_repu,
    mode='markers',
    name='Republicans',
    text=repu_hover_text,
    hoverinfo='text',
    marker=dict(
        symbol='dot',
        color=repu_color,
        size=repu_numConns,
        sizeref=2.*max(demo_numConns)/(10.**2),
        sizemin=3
    )
)

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

data = [edge_trace, node_trace_demo, node_trace_repu]

# create layout for plotly
layout = go.Layout(
         title="Sponsor-to-Cosponsor Network in the House",
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

# create figure with plotly
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='../Figures/HouseNetwork.html')

###########################################################
# create netowrk from connectivity matrix for Senate
G = nx.from_numpy_matrix(collabMat_sen)

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

# sort and add to lists x,y,z positions of nodes and hover text for plotly
Xn_demo = list()
Xn_repu = list()
Yn_demo = list()
Yn_repu = list()
Zn_demo = list()
Zn_repu = list()
adList = G.adjacency_list()
demo_hover_text = list()
repu_hover_text = list()
demo_numConns = list()
repu_numConns = list()
demo_color = list()
repu_color = list()
for i in range(0,len(senData)):
    thisName = senData.MemberFullName[i]
    thisParty = senData.MemberParty[i]
    thisNumConns = len(adList[i])
    if 'Dem' in thisParty:
        Xn_demo.append(Xn[i])
        Yn_demo.append(Yn[i])
        Zn_demo.append(Zn[i])
        demo_numConns.append(float(thisNumConns))
        demo_hover_text.append(('Name: ' + thisName + '<br>'+
                          'Party: ' + thisParty + '<br>'+
                          '# of Connections: ' + str(thisNumConns)))
        demo_color.append('rgb(56, 94, 244)')
    if 'Rep' in thisParty:
        Xn_repu.append(Xn[i])
        Yn_repu.append(Yn[i])
        Zn_repu.append(Zn[i])
        repu_numConns.append(float(thisNumConns))
        repu_hover_text.append(('Name: ' + thisName + '<br>'+
                          'Party: ' + thisParty + '<br>'+
                          '# of Connections: ' + str(thisNumConns)))
        repu_color.append('rgb(247, 59, 59)')

# create traces for plotly
node_trace_demo = go.Scatter3d(
    x=Xn_demo,
    y=Yn_demo,
    z=Zn_demo,
    mode='markers',
    name='Democrats',
    text=demo_hover_text,
    hoverinfo='text',
    marker=dict(
        symbol='dot',
        color=demo_color,
        size=demo_numConns,
        sizeref=2.*max(demo_numConns)/(10.**2),
        sizemin=3
    )
)

node_trace_repu = go.Scatter3d(
    x=Xn_repu,
    y=Yn_repu,
    z=Zn_repu,
    mode='markers',
    name='Republicans',
    text=repu_hover_text,
    hoverinfo='text',
    marker=dict(
        symbol='dot',
        color=repu_color,
        size=repu_numConns,
        sizeref=2.*max(demo_numConns)/(10.**2),
        sizemin=3
    )
)

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

data = [edge_trace, node_trace_demo, node_trace_repu]

# create layout for plotly
layout = go.Layout(
         title="Sponsor-to-Cosponsor Network in the House",
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
plotly.offline.plot(fig, filename='../Figures/SenateNetwork.html')
















##
##
##
