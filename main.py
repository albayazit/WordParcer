from requests import Session
from bs4 import BeautifulSoup as BS

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
}

TRANSLATED = []


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
    return all_pages

def get_page(URL):
    s = Session()
    s.headers.update(HEADERS)
    try:
        response = s.get(URL)
        with open('data.html', 'w', encoding='utf-8') as r:
            r.write(response.text)
    except:
        print("Network error!")
        
def get_word():
    words_list = []

    with open("data.html") as file:
        src = file.read()
    soup = BS(src, "lxml")

    words = soup.find(class_="words_list").find_all("a")

    for item in words:
        if (len(item.text) == 5):
            if ' ' in item.text or '-' in item.text:
                continue
            else:
                get_translate(item)
                words_list.append(item.text)

    return words_list

def get_translate(item):
    url = f"https://tatpoisk.net{item.get('href')}"
    translate = []
    s = Session()
    s.headers.update(HEADERS)
    response = s.get(url)
    soup = BS(response.text, "lxml")
    try:
        data = soup.find(class_="search_results").text.split(" ")
    except:
        print(item)
        return
    second = False
    translated = 0
    for i in data:
        if (not second):
            translate.append(i)
        if (len(i) > 4 and second == True):
            translate.append(i.replace(',', '').replace(';', '').replace(')', '').replace('(', ''))
            translated += 1
            if (translated == 2):
                break
        second = True

    if (len(translate) == 3):
        word = translate[0] + " - " + translate[1] + ", " + translate[2]
    else:
        try:
            word = translate[0] + " - " + translate[1]
        except:
            word = translate[0]
    
    TRANSLATED.append(word) 

def output():
    with open("words.txt", "w") as file:
        for item in TRANSLATED:
            file.write(item + "\n")

if __name__ == "__main__":
    get_page("https://tatpoisk.net/dict/tat2rus/list/ch")
    all_pages = get_all_pages()
    for page in all_pages:
        try:
            get_page(page)
            get_word()
        except:
            print(f"Error in {page}")
    get_word()
    for item in TRANSLATED:
        print(item)