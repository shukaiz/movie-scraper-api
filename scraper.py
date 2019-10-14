# coding=utf-8
import logging
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


# Configure logging level
logging.basicConfig(level=logging.INFO)
logging.debug("Program starts running")


# Use BeautifulSoup to parse start url.
start_url = requests.get("https://en.wikipedia.org/wiki/List_of_actors_with_Academy_Award_nominations").text
soup = BeautifulSoup(start_url, 'html.parser')
logging.debug("Read starting page and import into BeautifulSoup")


# Create lists to save all information scrapped from start url page.
name = []
gender = []
year_born = []
age = []
film = []
film_year = []
film_link = []
box_office = []
logging.debug("Lists created successfully")


# This part of the code first extract the table on
# the Wikipedia page and read all of the actor
# related information and save them into a list.

for entry in soup.find('table', {'class': 'sortable wikitable'}).find_all('tr')[1::1]:
    data = entry.find_all(['th', 'td'])
    try:
        name.append(data[0].a.text)
        gender.append(data[1].text)
        year_born.append(re.sub("[^0-9]", "", data[2].text))
        age.append(data[4].text)
        film.append(data[8].a.text)
        film_year.append(data[9].text)
        film_link.append(str("https://en.wikipedia.org" + data[8].a.get('href')))
    except IndexError:
        logging.warning("An IndexError has occurred.")
        pass


# Save all of the information from the
# table on starting page to data frame.

df = pd.DataFrame()
df['Name'] = name
df['Gender'] = gender
df['Born Year'] = year_born
df['Age'] = age
df['Film Name'] = film
df['Film Year'] = film_year
df['Film Link'] = film_link
logging.debug("Actor data have been saved into data frame successfully.")


# Save actor information to json.
df_actor = df[['Name', 'Gender', 'Born Year', 'Age']]
df_actor.to_json('json/actor.json', orient='records')
logging.info(r'Actor data have been saved to \actor.json')


# After the extraction of starting page, we
# got URLs for all of the films and in this
# part of the code, we will iterate through
# all of the URLs and retrieve film information
# from each individual wiki page (Box office).

for link in df['Film Link']:
    try:
        film_url = requests.get(link).text

        # Locate box office
        soup = BeautifulSoup(film_url, 'html.parser').find_all(string="Box office")[0].find_next()

        # Drop reference for grossing.
        extra_link = soup.find('a')
        _ = extra_link.extract()
        grossing = str(soup.text).replace('$', '').replace('£', '').replace(',', '') \
            .replace('–', ' million ').replace('US', '').split()

        # Add box office into a list. Multiply by 1 million if it is expressed by word 'million'.
        if 'million' in grossing[1]:
            print("Grossing: " + str(int(float(grossing[0]) * 1000000)))
            box_office.append(str(int(float(grossing[0]) * 1000000)))
        else:
            print("Grossing: " + str(int(float(grossing[0]))))
            box_office.append(str(int(float(grossing[0]))))

    # If error occurs when getting box office. Skips it and fill it with zero to indicate not available.
    except AttributeError:
        box_office.append(str(0))
        logging.warning("An AttributeError has occurred. Gross data for this movie is not available.")
        pass
    except IndexError:
        box_office.append(str(0))
        logging.warning("An IndexError has occurred. Gross data for this movie is not available.")
        pass
    except ValueError:
        box_office.append(str(0))
        logging.warning("A ValueError has occurred. Possibly not recognized format. "
                        "Gross data for this movie is not available.")
        pass


# Add grossing into data frame.
df['Box Office'] = box_office
logging.info(r'Grossing info have been added into data frame.')


# Save film information we have
# stored into data frame into json.

df_film = df[['Film Name', 'Film Year', 'Name', 'Box Office']]
df_film.to_json('json/film.json', orient='records')
logging.info(r'Film data have been saved to /film.json')
