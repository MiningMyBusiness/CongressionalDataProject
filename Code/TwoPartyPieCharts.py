# Make Pie charts for Democrat and Republican split in the House and senate
# Author: Kiran D. Bhattacharyya
# License: CC0


# import relevant libraries
import plotly.plotly as py
import plotly.graph_objs as go

# plot pie charts with plotly
fig = {
  "data": [
    {
      "values": [238,193], # number of republican and democratic members in the house
      "labels": [
        "Republican",
        "Democrat"
      ],
      'marker': {'colors': ['rgb(247, 59, 59)',
                                  'rgb(56, 94, 244)'
                                 ]},
      "domain": {"x": [0, .48]},
      "name": "House of Representatives",
      "hoverinfo":"label+value+name",
      "textinfo":"label+percent",
      "hole": 0,
      "type": "pie"
    },
    {
      "values": [51, 47, 2], # number of republican and democratic members in the senate
      "labels": [
        "Republican",
        "Democrat",
        "Independent"
      ],
      'marker': {'colors': ['rgb(247, 59, 59)',
                                  'rgb(56, 94, 244)',
                                  'rgb(59, 247, 240)'
                                 ]},
      "domain": {"x": [.52, 1]},
      "name": "Senate",
      "hoverinfo":"label+value+name",
      "textinfo":"label+percent",
      "hole": 0,
      "type": "pie"
    }],
  "layout": {
        "title":"Party Affiliations of Members in Congress",
    }
}
plotly.offline.plot(fig, filename='../Figures/HouseAndSenateSplit.html') # plot results
