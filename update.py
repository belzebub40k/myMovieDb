#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import json
import re

def searchList(regex, target):
   result = []
   for item in target:
      if re.search(regex, item):
         result.append(item)
   return result

conn = sqlite3.connect('MyVideos75.db')
conn.row_factory = sqlite3.Row

c = conn.cursor()

c.execute('SELECT \
            c00 AS title_local, \
            c01 AS plot, \
            c03 AS plot_outline, \
            c04 AS rating_votes, \
            c05 AS rating, \
            c06 AS writers, \
            c07 AS year, \
            c08 AS thumbnails, \
            c09 AS imdb_id, \
            c11 AS runtime, \
            c12 AS mpaa, \
            c13 AS imdb_top250, \
            c14 AS genre, \
            c15 AS director, \
            c16 AS title_original, \
            c18 AS studio, \
            c19 AS trailer, \
            c20 AS fanart, \
            c21 AS country, \
            idMovie,idFile,idSet \
         FROM movie \
         ORDER BY title_local;')

result = c.fetchall()

movie_list = { 'aaData': [] }

for movie in result:
   
   title_local = movie['title_local']
   title_original = movie['title_original']
   plot = movie['plot']
   plot_outline = movie['plot_outline']
   writers = movie['writers']
   director = movie['director']
   studio = movie['studio']
   thumbnails = searchList('w500', re.findall('http.*?\.jpg', movie['thumbnails']) )
   fanart = searchList('w780', re.findall('http.*?\.jpg', movie['fanart']) )
   rating = movie['rating'].rstrip('0').rstrip('.')
   rating_votes = re.sub(',', '.', movie['rating_votes'])
   runtime = "%02d" % divmod(int(movie['runtime']), 60)[0]
   year = movie['year']
   genre = movie['genre']
   country = movie['country']
   mpaa = movie['mpaa']
   imdb_id = movie['imdb_id']
   youtube_id = re.sub('&.*', '', re.sub('.*videoid=', '', movie['trailer']) )
   movie_id = movie['idMovie']
   file_id = movie['idFile']
   set_id = movie['idSet']
   
   
   movie_entry = {
      'title_local': title_local,
      'title_original': title_original,
      'plot': plot,
      'plot_outline': plot_outline,
      'writers': writers,
      'director': director,
      'studio': studio,
      'thumbnails': thumbnails,
      'fanart': fanart,
      'runtime': runtime,
      'rating': rating,
      'rating_votes': rating_votes,
      'year': year,
      'genre': genre,
      'mpaa': mpaa,
      'country': country,
      'imdb_id': imdb_id,
      'youtube_id': youtube_id }
   
   movie_file = open('data/' + str(movie_id) + '.json', 'w')
   movie_file.write(json.dumps(movie_entry,indent=2))
   movie_file.close()
   
   movie_list_enty = (
         title_local,
         rating,
         year,
         genre,
         country,
         movie_id )
   
   movie_list['aaData'].append(movie_list_enty)
   
movie_list_file = open('data/movie_list.json', 'w')
movie_list_file.write(json.dumps(movie_list,indent=2))
movie_list_file.close()
