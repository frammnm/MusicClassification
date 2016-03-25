# usual imports
import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np # get it at: http://numpy.scipy.org/
from pyechonest import config,track,song

config.ECHO_NEST_API_KEY="06SFFCURPOLZAR04N"

# path to the Million Song Dataset subset (uncompressed)
# CHANGE IT TO YOUR LOCAL CONFIGURATION
msd_subset_path='/home/francisco/Documents/Inteligencia/millionsongsubset_full/MillionSongSubset'
msd_subset_data_path=os.path.join(msd_subset_path,'data')
msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
assert os.path.isdir(msd_subset_path),'wrong path' # sanity check


# path to the Million Song Dataset code
# CHANGE IT TO YOUR LOCAL CONFIGURATION
msd_code_path='/home/francisco/Documents/Inteligencia/MusicClassification/MSongsDB'
assert os.path.isdir(msd_code_path),'wrong path' # sanity check

# we add some paths to python so we can import MSD code
# Ubuntu: you can change the environment variable PYTHONPATH
# in your .bashrc file so you do not have to type these lines
sys.path.append( os.path.join(msd_code_path,'PythonSrc') )


# imports specific to the MSD
import hdf5_getters as GETTERS


# the following function simply gives us a nice string for
# a time lag in seconds
def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))


# we define this very useful function to iterate the files
def apply_to_all_files(basedir,func=lambda x: x,ext='.h5'):
    """
    From a base directory, go through all subdirectories,
    find all files with the given extension, apply the
    given function 'func' to all of them.
    If no 'func' is passed, we do nothing except counting.
    INPUT
       basedir  - base directory of the dataset
       func     - function to apply to all filenames
       ext      - extension, .h5 by default
    RETURN
       number of files
    """
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files :
            func(f)  
    return cnt


# we can now easily count the number of files in the dataset
print 'number of song files:',apply_to_all_files(msd_subset_data_path)

# let's now get all artist names in a set(). One nice property:
# if we enter many times the same artist, only one will be kept.
songs = []

# we define the function to apply to all files
def func_to_get_artist_name(filename):
    """
    This function does 3 simple things:
    - open the song file
    - get artist ID and put it
    - close the file 
    """
    h5 = GETTERS.open_h5_file_read(filename)
    dictionary = {
        'artist_name': GETTERS.get_artist_name(h5),
        'artist_hotness': GETTERS.get_artist_hotttnesss(h5),
        'artist_familiarity': GETTERS.get_artist_familiarity(h5),
        'artist_id': GETTERS.get_artist_id(h5),
        'artist_mbid': GETTERS.get_artist_mbid(h5),
        'artist_playmeid': GETTERS.get_artist_playmeid(h5),
        'artist_7digitalid': GETTERS.get_artist_7digitalid(h5),
        'artist_latitude': GETTERS.get_artist_latitude(h5),
        'artist_longitude': GETTERS.get_artist_longitude(h5),
        'artist_location': GETTERS.get_artist_location(h5),
        'release': GETTERS.get_release(h5),
        'release_7digitalid': GETTERS.get_release_7digitalid(h5),
        'song_id': GETTERS.get_song_id(h5),
        'song_hotness': GETTERS.get_song_hotttnesss(h5),
        'title': GETTERS.get_title(h5),
        'danceability': GETTERS.get_danceability(h5),
        'duration': GETTERS.get_duration(h5),
        'energy': GETTERS.get_energy(h5),
        'key': GETTERS.get_key(h5),
        'key_confidence': GETTERS.get_key_confidence(h5),
        'loudness': GETTERS.get_loudness(h5),
        'mode': GETTERS.get_mode(h5),
        'mode_confidence': GETTERS.get_mode_confidence(h5),
        'tempo': GETTERS.get_tempo(h5),
        'time_signature': GETTERS.get_time_signature(h5),
        'time_signature_confidence': GETTERS.get_time_signature_confidence(h5),
        'track_id': GETTERS.get_track_id(h5)
    }
    songs.append(dictionary)
    h5.close()
    
# let's apply the previous function to all
# we'll also measure how long it takes
t1 = time.time()
apply_to_all_files(msd_subset_data_path,func=func_to_get_artist_name)
t2 = time.time()
print 'all artist names extracted in:',strtimedelta(t1,t2)

# t = track.track_from_id(songs[0]['track_id'])
# print t.artist_id

# t = track.track_from_id(songs[0]['track_id'])
# t.get_analysis
# print t


rkp_results = song.search(artist=songs[0]['artist_name'], title=songs[0]['title'])
print rkp_results

# let's see some of the content of 'all_artist_names'
# print 'found',len(all_artist_names),'unique artist names'
# for k in range(5):
#     print list(all_artist_names)[k]

# print filter(lambda x: x[:3] == 'get', hdf5_getters.__dict__.keys())

# # this is too long, and the work of listing artist names has already
# # been done. Let's redo the same task using an SQLite database.
# # We connect to the provided database: track_metadata.db
# conn = sqlite3.connect(os.path.join(msd_subset_addf_path,
#                                     'subset_track_metadata.db'))
# # we build the SQL query
# q = "SELECT DISTINCT artist_name FROM songs"
# # we query the database
# t1 = time.time()
# res = conn.execute(q)
# all_artist_names_sqlite = res.fetchall()
# t2 = time.time()
# print 'all artist names extracted (SQLite) in:',strtimedelta(t1,t2)
# # we close the connection to the database
# conn.close()
# # let's see some of the content
# # for k in range(5):
# #     print all_artist_names_sqlite[k][0]

# # now, let's find the artist that has the most songs in the dataset
# # what we want to work with is artist ID, not artist names. Some artists
# # have many names, usually because the song is "featuring someone else"
# conn = sqlite3.connect(os.path.join(msd_subset_addf_path,
#                                     'subset_track_metadata.db'))
# q = "SELECT * FROM songs"
# res = conn.execute(q)
# print res.fetchall()[0]
# #pop_artist_names = map(lambda x: x[0], res.fetchall())
# conn.close()
# print 'SQL query:',q
# #print 'name(s) of the most popular artist:',pop_artist_names
