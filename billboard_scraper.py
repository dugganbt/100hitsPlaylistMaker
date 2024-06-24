import requests
from bs4 import BeautifulSoup

def scrape_100_hits_for_date(date):

    content = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")

    soup = BeautifulSoup(content.text, "html.parser")

    # find the containers that contains the song and artist
    song_container = soup.find_all(class_="o-chart-results-list__item")

    song_artists = []

    # iterate over containers
    for container in song_container:
        try: # other containers not containing the id and class will cause an error
            song = container.find('h3', id='title-of-a-story').get_text(strip=True)
            artist = container.find('span', class_='c-label').get_text(strip=True)

            # Remove the origin of the song if added
            song = song.split('(From ')[0]

            # Keep only the main artist
            artist = artist.split(' Featuring')[0]
            artist = artist.split(' &')[0]

            # Remove whitespaces at beginning or end
            artist = artist.strip()
            song = song.strip()

            song_artists.append((song, artist))
        except AttributeError:
            continue

    return song_artists





