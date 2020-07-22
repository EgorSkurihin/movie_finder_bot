# -*- coding: utf-8 -*-

"""Class to work with TMDB API"""

import requests


class TMDB:

    def __init__(self, api_key):
        # Your TMDB API key
        self._tmdb_api_key = "?api_key=" + api_key

        # All using URLs
        self._url_base = "https://api.themoviedb.org/3/"
        self._url_all_genres = self._url_base + "genre/movie/list" + self._tmdb_api_key + "&language=ru-RU"
        self._url_search_movies = self._url_base + "discover/movie" + self._tmdb_api_key + "&language=ru-RU"
        self._url_movie_by_id = self._url_base + "movie/"
        self._url_similar_keywords = self._url_base + "search/keyword" + self._tmdb_api_key + "&language=ru-RU"

    def get_all_genres(self):
        # Return all movie genres in TMDB,
        # concatenated in list (elem = {name: <str>, id: <int>})
        response = requests.get(self._url_all_genres)
        return response.json()["genres"]

    def get_movies_by_genre(self, genre_id, page):
        # Gets id of genre and page number and return list of
        # movies from this page (elem = {title: <str>, id: <int>})
        full_url_genre_movies = self._url_search_movies + "&with_genres=" + str(genre_id) + "&page=" + str(page)
        response = requests.get(full_url_genre_movies).json()
        movie_list = []
        for i in range(len(response)):
            movie_list.append({})
            movie_list[i]["title"] = response["results"][i]["title"]
            movie_list[i]["id"] = response["results"][i]["id"]
        return movie_list

    def get_movie(self, movie_id):
        # Gets id of movie and return
        # description of this movie in dictionary
        full_url_movie_by_id = self._url_movie_by_id + str(movie_id) + self._tmdb_api_key + "&language=ru-RU"
        response = requests.get(full_url_movie_by_id)
        response = response.json()
        tmp = ""
        for genre in response["genres"]:
            tmp += genre["name"] + ", "
        response["genres"] = tmp[:len(tmp) - 2]
        return response

    def get_similar_keywords(self, keyword):
        # Gets key word and return similar key words with their id's,
        # concatenated in list (elem = {name: <str>, id: <int>})
        response = requests.get(self._url_similar_keywords + "&query=" + keyword)
        response = response.json()
        return response["results"]

    def get_movies_by_keyword(self, keyword_id):
        # works with the same principles as
        # get_movies_by_genre function but with keywords
        full_url_keyword_movies = self._url_search_movies + "&with_keywords=" + str(keyword_id) + "&page1"
        response = requests.get(full_url_keyword_movies)
        response = response.json()["results"]

        movie_list = []
        for i in range(len(response)):
            movie_list.append({})
            movie_list[i]["title"] = response[i]["title"]
            movie_list[i]["id"] = response[i]["id"]
        return movie_list
