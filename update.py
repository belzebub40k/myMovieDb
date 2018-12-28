#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import json
import re
import sys

channel_map = {
   0: '0.0',
   1: '1.0',
   2: '2.0',
   3: '2.1',
   4: '4.0',
   5: '4.1',
   6: '5.1',
   7: '6.1',
   8: '7.1',
   10: '9.1' }

def getResolution(width):
   if width > 1280:
      return 1080
   elif width > 960:
      return 720
   elif width > 720:
      return 540
   else:
      return 480

def searchList(regex, target):
   result = []
   for item in target:
      if re.search(regex, item):
         result.append(item)
   return result

conn = sqlite3.connect( sys.argv[1] )
conn.row_factory = sqlite3.Row

c = conn.cursor()

c.execute('SELECT \
            c00 AS title_local, \
            c01 AS plot, \
            c03 AS plot_outline, \
            c05 AS rating_id, \
            c06 AS writers, \
            c08 AS thumbnails, \
            c09 AS ident_id, \
            c11 AS runtime, \
            c12 AS mpaa, \
            c14 AS genre, \
            c15 AS director, \
            c16 AS title_original, \
            c18 AS studio, \
            c19 AS trailer, \
            c20 AS fanart, \
            c21 AS country, \
            premiered, \
            idMovie, \
            idFile, \
            idSet \
         FROM movie \
         ORDER BY title_local;')

result_movie = c.fetchall()

movie_list = { 'aaData': [] }

i = 0

for movie in result_movie:
   
   i = i + 1
   
   title_local = movie['title_local']
   title_original = movie['title_original']
   plot = movie['plot']
   plot_outline = movie['plot_outline']
   writers = movie['writers']
   director = movie['director']
   studio = movie['studio']
   thumbnails = searchList('w500', re.findall(r'http.*?\.jpg', movie['thumbnails']) )
   fanart = searchList('w780', re.findall(r'http.*?\.jpg', movie['fanart']) )
   runtime = "%02d" % divmod(int(movie['runtime']), 60)[0]
   genre = movie['genre']
   country = movie['country']
   mpaa = movie['mpaa']
   ident_id = movie['ident_id']
   youtube_id = re.sub('&.*', '', re.sub('.*videoid=', '', movie['trailer']) )
   premiered = movie['premiered']
   movie_id = movie['idMovie']
   file_id = movie['idFile']
   set_id = movie['idSet']
   
   
   c.execute('SELECT dateAdded FROM files WHERE idFile = ' + str(file_id) + ';')
   result_file = c.fetchone()   
   date_added = result_file['dateAdded'].split(' ')[0]


   c.execute('SELECT * FROM rating WHERE media_id = ' + str(movie_id) + ' AND rating_type = "imdb";')
   result_rating = c.fetchone()
   rating = result_rating['rating']
   votes = result_rating['votes']


   c.execute('SELECT * FROM streamdetails WHERE idFile = ' + str(file_id) + ';')
   result_stream = c.fetchall()

   streams = []
   resolution = 0

   for stream in result_stream:
      stream_entry = {}

      if stream['iStreamType'] == 0:
         stream_entry['type'] = 'v'
         stream_entry['codec'] = stream['strVideoCodec']
         stream_entry['aspect'] = stream['fVideoAspect']
         resolution = getResolution( stream['iVideoWidth'] )
         stream_entry['resolution'] = resolution
         stream_entry['stereo'] = stream['strStereoMode']

      if stream['iStreamType'] == 1: 
         stream_entry['type'] = 'a'
         stream_entry['codec'] = stream['strAudioCodec']
         stream_entry['language'] = stream['strAudioLanguage'].title()
         stream_entry['channels'] = channel_map[ stream['iAudioChannels'] ]

      if stream['iStreamType'] == 2: 
         stream_entry['type'] = 's'
         stream_entry['language'] = stream['strSubtitleLanguage'].title()

      streams.append(stream_entry)
   
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
      'genre': genre,
      'mpaa': mpaa,
      'country': country,
      'premiered': premiered,
      'ident_id': ident_id,
      'youtube_id': youtube_id,
      'date_added': date_added,
      'rating': rating,
      'votes': votes,
      'streams': streams }
   
   movie_file = open('data/' + str(movie_id) + '.json', 'w')
   movie_file.write(json.dumps(movie_entry,indent=2))
   movie_file.close()
   
   movie_list_enty = (
         title_local,
         genre,
         rating,
         premiered[0:4],
         date_added,
         movie_id )
   
   movie_list['aaData'].append(movie_list_enty)
   
movie_list_file = open('data/movie_list.json', 'w')
movie_list_file.write(json.dumps(movie_list,indent=2))
movie_list_file.close()

print("Exported " + str(i) + " Movies.")
