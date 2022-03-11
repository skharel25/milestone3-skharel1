import pdb
from typing import List
import flask
import requests
import os
import random
import pdb
from dotenv import find_dotenv, load_dotenv


def moviegetter(index):
    load_dotenv(find_dotenv())

    # A List of movie ids
    movids = [
        278,
        238,
        13,
        769,
        634649,
        7345,
        111,
        155,
        901,
        11,
        1891,
        1892,
        120,
        121,
        122,
    ]
    # Index to randomly traverse the list above
    index = index

    BASE_URL = "https://api.themoviedb.org/3/movie/"

    API_KEY = os.getenv("API_KEY")

    params = {"api-key": API_KEY}

    response = requests.get(
        BASE_URL + str(movids[index]) + "?api_key=" + API_KEY + "&language=en-US"
    )

    response_json = response.json()

    # A list containing all of the info we want from the api call
    info = []

    try:
        info.append((response_json["original_title"]))

    except KeyError:
        return "Couldn't fetch this data!"

    try:
        info.append(response_json["tagline"])

    except KeyError:
        return "Couldn't fetch this data!"

    try:
        info.append(response_json["genres"])

    except KeyError:
        return "Couldn't fetch this data!"

    try:
        info.append(response_json["poster_path"])
    except KeyError:
        return "Couldn't fetch this data"

    try:
        info.append(response_json["id"])
    except KeyError:
        return "Couldn't fetch this data"

    return info

