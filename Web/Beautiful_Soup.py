from bs4 import BeautifulSoup
import requests

yc_news_page = requests.get('https://news.ycombinator.com').text
# print(yc_news_page)

titles = []
soup = BeautifulSoup(yc_news_page, 'html.parser')
title_tags = soup.select('.titleline')
for title_tag in title_tags:
    a_tag = title_tag.find('a')
    # print(f'title: {title_tag.getText()} link: {a_tag.get("href")}')
    titles.append([title_tag.getText(), a_tag.get("href")])

scores = []
score_tags = soup.select('.score')
for score_tag in score_tags:
    scores.append(int(score_tag.getText().split()[0]))

results = [(s, *t) for s, t in zip(scores, titles)]
# [print(r) for r in results]

most_upvoted_article = max(results, key=lambda x: x[0])
print(most_upvoted_article)
