"""Main bot file"""

import telebot
import config
import messages
import bot_functions


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_start_info(message):
    message_start = bot_functions.send_start_message()
    bot.send_message(message.chat.id, message_start[0], reply_markup=message_start[1])


@bot.message_handler(content_types=['text'])
def send_info_movie(message):
    if message.text == "Жанры":
        message_genres = bot_functions.send_genres_message()
        bot.send_message(message.chat.id, message_genres[0], reply_markup=message_genres[1])

    elif message.text.startswith("/mv"):
        try:
            movie_info = bot_functions.send_movie_info(message.text[3:])
            bot.send_message(message.chat.id, movie_info)
        except:
            bot.send_message(message.chat.id, messages.error_movie_message)

    else:
        try:
            similar_keywords = bot_functions.send_similar_keywords(message.text)
            bot.send_message(message.chat.id, similar_keywords[0], reply_markup=similar_keywords[1])
        except:
            bot.send_message(message.chat.id, messages.error_keyword_message)


@bot.callback_query_handler(func=lambda call: True)
def genre_callback_query(call):
    page_number = 1
    genre_id = ""
    try:
        if call.data.startswith("g"):
            genre_id = call.data[1:]
            page_number = 1
            movies = bot_functions.send_movies_by_genre(genre_id, page_number)
            bot.send_message(call.from_user.id, movies[0], reply_markup=movies[1])

        elif call.data == "next":
            page_number += 5
            movies = bot_functions.send_movies_by_genre(genre_id, page_number)
            bot.send_message(call.from_user.id, movies[0], reply_markup=movies[1])

        elif call.data.startswith("k"):
            movies = bot_functions.send_movies_by_keyword(call.data[1:])
            bot.send_message(call.from_user.id, movies)
    except:
        bot.send_message(call.from_user.id, messages.error_button_message)


if __name__ == '__main__':
    bot.polling(none_stop=True)