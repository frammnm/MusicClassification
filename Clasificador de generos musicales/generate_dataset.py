# Archivo: generate_dataset.py
# Este es archivo contiene el script para obtener el data set de las canciones
# utilizando la libreria Pyechonest del API Echonest.
# Autores: 
#    - Francisco Martinez 09-10502
#    - Gabriel   Alvarez  09-10029

from pyechonest import config, song, track,  playlist
import time
import random

#API Key
config.ECHO_NEST_API_KEY = '06SFFCURPOLZAR04N'

genres = ['metal','jazz','rap','electronic']

def get_songs(g):

    time.sleep(60)
    print (g,"GENRE")
    i = 0 
    while (i <= 60 ):
        try: 
            p = playlist.static(genres=g,type="genre-radio", results=15)
            for s in p:    
                print (s,"SONG")
                dictionary = s.get_audio_summary()
                track = []
                track.append(s.artist_name.encode('ascii','ignore'))
                track.append(dictionary['danceability'])
                track.append(dictionary['duration'])
                track.append(dictionary['energy'])
                track.append(dictionary['key'])
                track.append(dictionary['liveness'])
                track.append(dictionary['loudness'])
                track.append(dictionary['mode'])
                track.append(dictionary['speechiness'])
                track.append(dictionary['tempo'])
                track.append(dictionary['time_signature'])
                track.append(g)
                songs.append(track)
            i +=1
            time.sleep(60)
        except:
            print ("Connection lost!, reconnecting...")
            time.sleep(60)
            pass 

def generate_data_set(filename):
    try:
        f = open(filename,'a')
        f.write("artist\tdanceability\tduration\tenery\tkey\tliveness\tloudness\tmode\tspeechiness\ttempo\ttime_signature\tgenre\n") 
        f.write("d\tc\tc\tc\td\tc\tc\td\tc\tc\td\td\n")
        f.write("\t\t\t\t\t\t\t\t\t\t\tclass\n")
        for track in songs:
            for atribute in track:
                f.write(str(atribute)) 
                f.write("\t")
            f.write("\n")
        f.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit(1)

def run_main():
    for g in genres :
        songs = [] 
        get_songs(g)
        generate_data_set("songs_data_set.tab");
        print "Saving progress..."

if __name__ == "__main__":
    run_main()