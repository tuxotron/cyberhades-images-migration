
import re
from os import listdir
from os.path import isfile, join

def replaceImg(entry, dict):
    f = open(entry, "r", encoding = "ISO-8859-1")
    c = f.read()
    f.close()
    matches = re.findall("http[s]?://farm?.\.static\.*flickr\.com/\d+/\d+_\w+\.[a-z]{3,4}", c)
    matches = matches + re.findall("http[s]?://www\.flickr\.com/photos/cyberhades/\d+/*", c)
    matches = matches + re.findall("http[s]?://c?.\.staticflickr\.com/\d+/\d+/\d+_\w+\.[a-z]{3,4}", c)

    # print(matches)
    
    for match in matches:
        if '_' in match:
            k = match.split('/')[-1].split('_')[0]
        else:
            tokens = match.split('/')
            if tokens[-1].isdigit():
                k = tokens[-1]
            else:
                k = tokens[-2]

        if k in dict:
            c = c.replace(match, "https://cyberhades.ams3.cdn.digitaloceanspaces.com/imagenes/" + dict[k])
    
    print(entry)
    o = open(entry, "w", encoding = "ISO-8859-1")
    o.write(c)
    o.close()


def loadFilenames(picspath):

    dict = {}
    
    onlyfiles = [f for f in listdir(picspath) if isfile(join(picspath, f))]
    for entry in onlyfiles:
        tokens = entry.split("_")
        if tokens[-3].isdigit():
            dict[tokens[-3]] = entry
        if len(tokens) > 3 and tokens[-4].isdigit():
            dict[tokens[-4]] = entry

    return dict

if __name__ == "__main__":
    mypath = 'DIRECTORIO CON LAS ENTRADAS'
    picspath = 'DIRECTORIO CON LAS FOTOS'

    dict = loadFilenames(picspath)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for entry in onlyfiles:
        replaceImg(mypath + entry, dict)

