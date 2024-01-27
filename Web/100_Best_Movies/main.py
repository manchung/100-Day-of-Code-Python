from bs4 import BeautifulSoup
import requests, os

movie_webpage = requests.get('https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/')

soup = BeautifulSoup(movie_webpage.text, 'html.parser')
# print(soup.select('h3.title'))

titles = [tag.getText() for tag in soup.select('h3.title')]
titles.reverse()
# print(titles)

output_filename = os.path.join(os.path.dirname(__file__), 'movies.txt')
with open(output_filename, 'w') as file:
    [file.write(f'{t}\n') for t in titles]
