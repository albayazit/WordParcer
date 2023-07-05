from requests import Session
from bs4 import BeautifulSoup as BS


def get_all_pages():
    all_pages = []

    with open("data.html") as file:
        src = file.read()

    soup = BS(src, "lxml")
    pages_list = soup.find(class_="search").find_all("a")
    for item in pages_list:
        all_pages.append("https://tatpoisk.net" + item.get("href"))
        if (len(all_pages) == 34):
            break
    print(all_pages)

def get_page(URL):
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
    }
    s = Session()
    s.headers.update(HEADERS)
    try:
        response = s.get(URL)
        with open('data.html', 'w', encoding='utf-8') as r:
            r.write(response.text)
    except:
        print("Network error!")


if __name__ == "__main__":
    get_page("https://tatpoisk.net/dict/tat2rus/list/a")
    get_all_pages()