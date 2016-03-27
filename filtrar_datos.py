# usual imports
import os
import sys
import time

songs = []
MAX_NUM_PER_GENRE = 900

def filtrar(filename,newfilename): 
    try:
        f1 = open(filename,'r')
        f2 = open(newfilename,'a')
        data = f1.readlines()
        i = 0 
        m = 0
        j = 0
        r = 0 
        e = 0 
        f2.write("artista\tdanceability\tduration\tenery\tkey\tliveness\tloudness\tmode\tspeechiness\ttempo\ttime_signature\tgenre\n") 
        f2.write("s\tc\tc\tc\td\tc\tc\td\tc\tc\td\ts\ts\n")
        f2.write("\t\t\t\t\t\t\t\t\t\t\tclass\n")
        for line in data:
            if i > 2 :
                words = line.split('\t')
                if words[11] == "metal":
                    if m < MAX_NUM_PER_GENRE:
                        f2.write(line)
                    m += 1
                if words[11] == "jazz":
                    if j < MAX_NUM_PER_GENRE:
                        f2.write(line)
                    j += 1
                if words[11] == "rap":
                    if r < MAX_NUM_PER_GENRE:
                        f2.write(line)
                    r += 1
                if words[11] == "electronic":
                    if e < MAX_NUM_PER_GENRE:
                        f2.write(line)
                    e += 1
            i += 1

        f1.close()
        f2.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit(1)


def run_main():
    filtrar("songs_data_set.tab","balanced_songs_data_set.tab")

if __name__ == "__main__":
    run_main()