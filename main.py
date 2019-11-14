from bs4 import BeautifulSoup
import requests
import re
import json
url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.posterColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
imdb = []

# Stored each item into dictionary
for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
    link= 'https://www.imdb.com'+links[index]
    direc=crew[index].split('(dir.),')
    data = {"name": movie_title,
            "rating": ratings[index],
            "release": year,
            "director": direc[0],
            "stars":direc[1],
            "link": link
            }
    imdb.append(data)
imdbdata=json.dumps(imdb)
with open('data.json', 'w') as f:
    json.dump(imdb, f)
print(imdb)
