import json
import math
import numpy as np
import plotly.graph_objects as go
import networkx as nx

# colors
BLACK = "#332C39"
RED = "#DC0000"
PURPLE = "#A555EC"
GREEN = "#16FF00"
NODES = "#3F979B"
NORMALSIZE = 1
FLAGGEDSIZE = 4

PLOTLY_OUTPUT_FILE = "./index.html"


def get_master_trace_list(masterConfig: dict) -> list:
    # initialize
    masterTraceList = []

    # compile traces from all sites
    for customer in masterConfig:
        sites = masterConfig[customer]
        for site in sites:
            # append new ones, keep only unique ones
            masterTraceList += sites[site]
            masterTraceList = np.unique(masterTraceList).tolist()
    return masterTraceList


def get_max_num_sites(masterConfig: dict) -> list:
    # initialize
    maxNumSites = 0

    # compile traces from all sites
    for customer in masterConfig:
        sites = masterConfig[customer]
        maxNumSites = max(maxNumSites, len(sites))
    return maxNumSites


def get_square_area_positions(
                            elements: list = None,
                            rootPos: int = 0,
                            zSpace: int = 1,
                            planarSpace: int = 1,
                            ) -> 'list[list]':
    if elements is None:
        return None

    # get dimension of square
    dimSize = math.ceil(math.sqrt(len(elements)))
    halfDimSize = math.ceil(0.5 * dimSize)

    # assemble single dimension lengths
    lwr = -1*planarSpace*halfDimSize
    upr = halfDimSize*planarSpace+1
    stp = planarSpace
    planePositions = list(range(lwr, upr, stp))
    planePositions.pop(planePositions.index(0))

    # assemble pland of positions
    pos = []
    for pos1 in planePositions:
        for pos2 in planePositions:
            pos.append([rootPos[0]+pos1, rootPos[1]+pos2, rootPos[2]-zSpace])
    return pos


# main
def main():
    # default values
    # TODO: Use a parser to allow user to supply
    rootPos = [0, 0, 0]
    zSpaceCustomer = 4
    zSpaceSite = 6
    zSpaceTrace = 20
    traceSquareSpacing = 4
    siteSquareSpacing = 2
    customerSquareSpacing = 8
    nodeSize = 5

    # initialization
    customerZSpace = rootPos[2] + zSpaceCustomer
    siteZSpace = customerZSpace + zSpaceSite
    traceZSpace = siteZSpace + zSpaceTrace

    # read connection and data files
    # TODO reduce this into less code, put into function
    with open('dataPresent.json') as f1:
        dataPresent = json.load(f1)

    with open('connections.json') as f2:
        connections = json.load(f2)

    with open('siteStatus.json') as f3:
        siteStatus = json.load(f3)

    # get master list of traces
    masterTraceList = get_master_trace_list(connections)

    # ---------------- Network Generation -------------------------
    # ---------------- Network Generation -------------------------
    # initialization
    G = nx.MultiGraph()

    # add nodes for traces
    tPos = get_square_area_positions(
        elements=masterTraceList,
        rootPos=rootPos,
        planarSpace=traceSquareSpacing,
        zSpace=traceZSpace
    )
    for idx, t in enumerate(masterTraceList):
        G.add_node(
            node_for_adding=t,
            nodeType="trace",
            displayName=t,
            pos=tPos[idx]
        )

    # add node for axiom cloud main node
    G.add_node(
        node_for_adding="root",
        nodeType="root",
        displayName="Company NAME",
        pos=rootPos
    )

    # add nodes and edges for site configurations
    # --- customers
    population = get_max_num_sites(connections)
    cDist = math.ceil(math.sqrt(population)) + 1 + siteSquareSpacing
    customerSquareSpacing = max(cDist, customerSquareSpacing)
    customerPos = get_square_area_positions(
        elements=connections.keys(),
        rootPos=rootPos,
        planarSpace=customerSquareSpacing,
        zSpace=customerZSpace
    )
    for cIdx, customer in enumerate(connections):
        G.add_node(
            node_for_adding=customer,
            nodeType="customer",
            displayName=customer,
            pos=customerPos[cIdx]
        )
        G.add_edge("root", customer, color=BLACK)

        # --- sites
        sites = connections[customer]
        sitePos = get_square_area_positions(
            elements=sites,
            rootPos=customerPos[cIdx],
            planarSpace=siteSquareSpacing,
            zSpace=siteZSpace
        )
        for sIdx, site in enumerate(sites):
            G.add_node(
                node_for_adding=site,
                nodeType="site",
                displayName=site,
                pos=sitePos[sIdx]
            )
            if site in siteStatus[customer]["BCU"]:
                G.add_edge(customer, site, color=GREEN)
            elif site in siteStatus[customer]["In Progress"]:
                G.add_edge(customer, site, color=PURPLE)
            else:
                G.add_edge(customer, site, color=RED)

            for trace in masterTraceList:
                if trace in connections[customer][site]:
                    if trace not in dataPresent[customer][site]:
                        G.add_edge(site, trace, color=RED)
                    else:
                        G.add_edge(site, trace, color=GREEN)
    # ---------------- Network Generation -------------------------
    # ---------------- Network Generation -------------------------

    # ---------------- Network Phenotyping ------------------------
    # ---------------- Network Phenotyping ------------------------
    # initialization
    traceList = []
    node_x = []
    node_y = []
    node_z = []
    nodeNames = []

    # --- assemble list of edge traces
    for src, dst, color in G.edges(data="color"):
        # grab to-from coordinates
        x0, y0, z0 = G.nodes[src]['pos']
        x1, y1, z1 = G.nodes[dst]['pos']

        # set width based on coloring
        width = NORMALSIZE
        if color not in [BLACK, GREEN]:
            width = FLAGGEDSIZE

        # add edge to trace list
        traceList.append(
            go.Scatter3d(
                x=[x0, x1],
                y=[y0, y1],
                z=[z0, z1],
                line={"width": width, "color": color},
                hoverinfo='none',
                mode='lines'
            )
        )

    # --- assemble list of nodes
    for node, nodeName in G.nodes(data="displayName"):
        x, y, z = G.nodes[node]['pos']
        nodeNames.append(nodeName)
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    # put nodes into a single trace
    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode='markers+text',
        hoverinfo='text',
        hovertext=None,
        textposition='top center',
        marker=dict(
            color=[],
            size=nodeSize,
            line_width=2)
    )

    # node attributes
    node_trace.marker.color = "#3F979B"
    node_trace.text = nodeNames
    # ---------------- Network Phenotyping ------------------------
    # ---------------- Network Phenotyping ------------------------

    # ---------------- Generate Plotly HTML -----------------------
    # ---------------- Generate Plotly HTML -----------------------
    # add node scatters to list of traces to plot
    traceList.append(node_trace)

    # create graph
    fig = go.Figure(
        data=traceList,
        layout=go.Layout(
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, visible=False),
            yaxis=dict(showbackground=False, visible=False),
            zaxis=dict(showbackground=False, visible=False),
            bgcolor='white'
        ),
    )
    fig.write_html(
        PLOTLY_OUTPUT_FILE,
        full_html=False,
        include_plotlyjs='cdn'
    )
    # ---------------- Generate Plotly HTML -----------------------
    # ---------------- Generate Plotly HTML -----------------------


if __name__ == '__main__':
    main()
else:
    pass
