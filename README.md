![Plotly](https://camo.githubusercontent.com/d4b85dc983c64c148504c0aea59d9cefa65b75a8e538d932c592f2fca15b3b82/68747470733a2f2f696d616765732e706c6f742e6c792f6c6f676f2f706c6f746c796a732d6c6f676f4032782e706e67)
![NetworkX](https://networkx.org/_static/networkx_logo.svg)
# Plotly Data Plotting Example
---
## Purpose
This repo is one of a collection of repos that I have to exhibit my programming/technical skills. In this repo, I exhibit the following:

1. Ability to design a code to accomplish a workplace tool.
2. Use of JSON in python.
3. Use of ```networkx``` package to develop relationships between data.
4. Design of unique network spacing algorithm to space out each layer for visibility.
5. Use of ```plotly``` to visualize data.
6. Conversion from ```networkx``` to ```plotly```.
7. Use of appropriate color scheme and layout practices.
8. Generation of standalone HTML file that visualizes data in 3D, interactive format.
9. Understanding of the use of CDN in lieu of hard-copies of web styling files.

## Installation/Setup
This repo is simple, and requires only a few packages. You can set up the repo using the requirements text file provided in the code package. Follow these steps to get this repo up and running on your local machine:

1. Clone the repo to your machine.
2. Navigate to the repo on your machine.
3. Activate your python virtual environment (venv).
4. Install the required packages to your venv:
    ```powershell
    pip install -r requirements.txt
    ```

## Code Files
There are a few hard-coded files that the main script is going to expect. These files can be changed by a user if the user would like to observe different behaviors from adding/removing information from the files. The following are those files:
1. ```siteStatus.json``` - file intended to summarize the state of the site (i.e., "BCU" = "a customer site is up and running"; and "In Progress" = "customer is in the process of being entered into our database, but is not up and running"). The values in this file change the lines between the ```customer``` and ```customer-branch``` layers. The line is green if ```customer-branch``` is listed as ```BCU```; is purple if ```customer-branch``` is listed as ```In Progress```; and is red if ```customer-branch``` is NOT listed in siteStatus.json.
2. ```connections.json``` - file intended to summarize all of the data traces the customer should be connected to.
3. ```dataPresent.json``` - file intended to summarize all of the data that traces the customer is actually receiving.

NOTE: Differences between information in [2] and [3] above will determine if the line is red (data trace is missing from ```customer-branch```), is green (data trace is prsent for ```customer-branch```).

## Code Execution
The code is relatively simple. The intention was to show example of knowledge, so it is kept to the simple execution of the main script, which is entitled ```data_viz_tool.py```. You can run this script using the following:

    python .\data_viz_tool.py

