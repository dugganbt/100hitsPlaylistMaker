import requests
from bs4 import BeautifulSoup

# date = input("Enter the date (YYYY-MM-DD) from which you would like to create the hits playlist: ")

date = "1996-05-10"

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
        song_artists.append((song, artist))
    except AttributeError:
        continue

print(song_artists)