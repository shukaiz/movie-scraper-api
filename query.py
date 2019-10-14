import pandas as pd
import logging

# Configure logging level
logging.basicConfig(level=logging.WARNING)

# Read json as data frame.
actor_df = pd.read_json('json/actor.json')
film_df = pd.read_json('json/film.json')
logging.debug("JSON read successfully.")


# Find how much a movie has grossed
def total_gross(film_name):
    logging.debug("total_gross function called.")
    df = film_df[film_df['Film Name'] == film_name]
    return str(df['Box Office'].iloc[0])


# List which movies an actor has worked in
def movie_worked(actor_name):
    logging.debug("movie_worked function called.")
    df = film_df[film_df['Name'] == actor_name]
    return str(df['Film Name'].iloc[0])


# List which actors worked in a movie
def which_actor(film_name):
    logging.debug("which_actor function called.")
    df = film_df[film_df['Film Name'] == film_name]
    return str(df['Name'].values.tolist())


# List the top X actors with the most total grossing value
def top_actors(x):
    logging.debug("top_actors function called.")
    df = film_df.nlargest(x, 'Box Office')
    return str(df['Name'].values.tolist())


# List the oldest X actors
def old_actors(x):
    logging.debug("old_actors function called.")
    df = actor_df.nlargest(x, 'Age')
    return str(df['Name'].values.tolist())


# List all the movies for a given year
def movies_in_year(year):
    logging.debug("movies_in_year function called.")
    df = film_df[film_df['Film Year'] == year]
    return str(df['Film Name'].values.tolist())


# List all the actors for a given year
def actors_in_year(year):
    logging.debug("actors_in_year function called.")
    df = film_df[film_df['Film Year'] == year]
    return str(df['Name'].values.tolist())


# Find how much a movie has grossed
print('This movie have grossed ' + total_gross('Amadeus'))

# List which movies an actor has worked in
print('This actor/actress have worked in ' + movie_worked('Catherine Zeta-Jones'))

# List which actors worked in a movie
print('Actors/actresses worked in this movie are ' + which_actor('Roma'))

# List the top X actors with the most total grossing value
print('Top 10 actors/actresses with most total grossing value are ' + top_actors(10))

# List the oldest X actors
print('Top 10 oldest actors/actresses ' + old_actors(10))

# List all the movies for a given year
print('Movies in 2010 are ' + movies_in_year(2010))

# List all the actors for a given year
print('Actors/actresses in 2018 are ' + actors_in_year(2018))
