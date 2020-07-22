# -*- coding: utf-8 -*-

"""
Functions that bot use
All of them return tuple of 2 elements (except send_movie_info, send_movies_by_keyword):
text to send and keyboard
"""

from tmdb import TMDB
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import messages
import config

tmdb_obj = TMDB(config.API_KEY)


def send_start_message():
    # Sends key "Genres" and start message
    search_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    search_keyboard.row("Жанры")
    return messages.start_message, search_keyboard


def send_genres_message():
    # Sends genres callback keyboard
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    genres = tmdb_obj.get_all_genres()
    for i in range(0, len(genres)-1, 2):
        markup.add(InlineKeyboardButton(genres[i]["name"], callback_data="g" + str(genres[i]["id"])),
                   InlineKeyboardButton(genres[i+1]["name"], callback_data="g" + str(genres[i+1]["id"])))
    return "Выбор жанра: ", markup


def send_movies_by_genre(genre_id, page):
    # Send 4 pages of movies in this genre starts with this page
    message = "\U0001F447Фильмы по этому жанру:\U0001F447 \n"
    film_number = 1
    for i in range(5):
        movies = tmdb_obj.get_movies_by_genre(genre_id, page + i)
        for j in range(4):
            message += str(film_number) + ". " + movies[j]["title"] + " - (" + "/mv" + str(movies[j]["id"]) + ")\n"
            film_number += 1

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Следующая страница >>", callback_data="next"))
    return message, markup


def send_movie_info(movie_id):
    # Send information about movie with this id
    movie_info = tmdb_obj.get_movie(movie_id)
    return messages.movie_information.substitute(movie_info)


def send_similar_keywords(keyword):
    # Send callback keyboard with similar keywords
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    keywords = tmdb_obj.get_similar_keywords(keyword)
    for i in range(0, len(keywords)-1, 2):
        markup.add(InlineKeyboardButton(keywords[i]["name"], callback_data="k" + str(keywords[i]["id"])),
                   InlineKeyboardButton(keywords[i+1]["name"], callback_data="k" + str(keywords[i+1]["id"])))
    return "Выберете наиболее подходящий вариант: ", markup


def send_movies_by_keyword(keyword_id):
    # Send movies by keyword
    movies = tmdb_obj.get_movies_by_keyword(keyword_id)
    message = "\U0001F447Фильмы по этому ключевому слову:\U0001F447 \n"
    for i in range(len(movies)):
        message += str(i+1) + ". " + movies[i]["title"] + " - (" + "/mv" + str(movies[i]["id"]) + ")\n"
    return message
