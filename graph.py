import numpy as np
import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json
import logging


def top_actors(x):
    """
    List the top X actors with most movie productions
    With most movie productions means more connections.
    """
    logging.debug("top_actors function called.")
    df = df_actor.nlargest(x, 'num_movies')
    return str(df['name'].values.tolist())


def print_edges(g):
    """
    Print all edges in the graph
    For testing.
    """
    logging.debug("print_edges function called.")
    for line in nx.generate_adjlist(g):
        print(line)


def data_analysis():
    """
    Plot relationship between age and total gross.
    Also conducts data analysis as required.
    """
    logging.debug("data_analysis function called.")

    plt.scatter(df_actor['age'], df_actor['total_gross'], s=df_actor['num_movies'], alpha=0.5)
    plt.title("Actor/Actresses' Age vs. Total Gross")
    plt.xlabel("Age")
    plt.ylabel("Total Gross")
    plt.show()

    print(top_actors(2))  # List out two actors with most connections.

    print("Correlation between actor/actress' age and total gross:")
    print(np.corrcoef(df_actor['age'], df_actor['total_gross']))


data = json.load(open("json/data.json"))  # Read new JSON
logging.debug("data.json Read.")

graph = nx.Graph()  # Initialize graph

# Create new lists for actors to be added to data frame.
name = []
age = []
total_gross = []
movies = []

# To generate JSON for later visualization.
id = []
group = []
source = []
target = []
value = []

# Read actor data and add to graph
for i in data[0]:
    name.append(i)
    id.append(i)
    group.append(1)
    age.append(data[0][i]['age'])
    total_gross.append(data[0][i]['total_gross'])
    movies.append(len(data[0][i]['movies']))
    graph.add_node(i)
    for movie in data[0][i]['movies']:
        graph.add_node(movie)
        graph.add_edge(i, movie)
        id.append(movie)
        group.append(2)
        source.append(i)
        target.append(movie)
        value.append(5)
logging.info("Actor data read and added to graph.")

# Create a data frame for actors
df_actor = pd.DataFrame()
df_actor['name'] = name
df_actor['age'] = age
df_actor['total_gross'] = total_gross
df_actor['num_movies'] = movies

# Create new lists for films to be added to data frame.
film = []
year = []
box_office = []
actors = []

# Read film data
for i in data[1]:
    film.append(i)
    id.append(i)
    group.append(2)
    year.append(data[1][i]['year'])
    box_office.append(data[1][i]['box_office'])
    actors.append(len(data[1][i]['actors']))
    graph.add_node(i)
    for actor in data[1][i]['actors']:
        graph.add_node(actor)
        graph.add_edge(i, actor)
        id.append(actor)
        group.append(1)
        source.append(i)
        target.append(actor)
        value.append(5)
logging.info("Movie data read and added to graph.")

# Create a data frame for films
df_movie = pd.DataFrame()
df_movie['name'] = film
df_movie['year'] = year
df_movie['box_office'] = box_office
df_movie['num_actors'] = actors

# Generate node JSON for visualization
df_nodes = pd.DataFrame()
df_nodes['id'] = id
df_nodes['group'] = group
df_nodes.to_json('json/nodes.json', orient='records')

# Generate links JSON for visualization
df_links = pd.DataFrame()
df_links['source'] = source
df_links['target'] = target
df_links['value'] = value
df_links.to_json('json/links.json', orient='records')

# Run for data analysis
data_analysis()
