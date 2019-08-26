from bs4 import BeautifulSoup
import requests
import json

agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}
base = "https://www.azlyrics.com/"

#Set the variable to the name of the artist that you want to download
artist_name = "Artist name"

def artists(letter):
    if letter.isalpha() and len(letter) is 1:
        letter = letter.lower()
        url = base + letter + ".html"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        data = []

        for div in soup.find_all("div", {"class": "container main-page"}):
            links = div.findAll('a')
            for a in links:
                data.append(a.text.strip())
        return json.dumps(data)
    else:
        raise Exception("Unexpected Input")


def songs(artist):
    artist = artist.lower().replace(" ", "")
    first_char = artist[0]
    url = base + first_char + "/" + artist + ".html"
    req = requests.get(url, headers=headers)

    artist = {
        'artist': artist,
        'albums': {}
    }

    soup = BeautifulSoup(req.content, 'html.parser')

    all_albums = soup.find('div', id='listAlbum')
    first_album = all_albums.find('div', class_='album')
    album_name = first_album.b.text
    s = []

    for tag in first_album.find_next_siblings(['a', 'div']):
        if tag.name == 'div':
            artist['albums'][album_name] = s
            s = []
            if tag.b is None:
                pass
            elif tag.b:
                album_name = tag.b.text

        else:
            if tag.text is "":
                pass
            elif tag.text:
                s.append(tag.text)

    artist['albums'][album_name] = s

    return json.dumps(artist)


def lyrics(artist, song):
    artist = artist.lower().replace(" ", "")
    song = song.lower().replace(" ", "")
    url = base + "lyrics/" + artist + "/" + song + ".html"

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    l = soup.find_all("div", attrs={"class": None, "id": None})
    if not l:
        return {'Error': 'Unable to find ' + song + ' by ' + artist}
    elif l:
        l = [x.getText() for x in l]
        return l


with open("songlyrics.txt", "r") as file:
    songs = []
    for line in file:
        songs.append(line[0:len(line)-1])

for i in range(len(songs)):
    wd = lyrics(artist_name, str(songs[i]))
    print (wd)
    for line in wd:
        with open('songlyrics.txt', 'a') as file:
            file.write(line)
