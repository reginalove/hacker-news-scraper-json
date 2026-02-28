import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

url = "https://news.ycombinator.com/"

headers = {
        "user-agent": "mozilla/5.0"
           }

list_gossib = []

while url:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    page = soup.select("tr.athing")

    for each in page:
       meta_row = each.find_next_sibling("tr")

       title = each.select_one("span.titleline").get_text(strip=True)
       link = each.select_one("span.titleline a")["href"]

       score_tag = meta_row.select_one("span.score")
       score = score_tag.get_text(strip=True) if score_tag else "0 points"

       author_tag = meta_row.select_one("a.hnuser")
       author = author_tag.get_text(strip=True) if author_tag else None

       subline = meta_row.select_one("span.subline")
       the_links = subline.find_all("a")
       comments = 0
       for comment in the_links:
           text = comment.get_text(strip=True)
           if "comment" in text:
               comments = int(text.split()[0])

       gossibs = {"title": title,
                  "link": link,
                  "author": author,
                  "score": score,
                  "comments": comments,}
       list_gossib.append(gossibs)
    next_page = soup.select_one("a.morelink")
    if not next_page:
       break
    url = urljoin(url, next_page["href"])



with open("gossibs.json", "w", encoding="utf-8") as f:
    json.dump(list_gossib, f, ensure_ascii=False)



