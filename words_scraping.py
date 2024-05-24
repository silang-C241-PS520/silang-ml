from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def word_scraping():
    NUM_PAGE = 107
    TEMPLATE_URL = "https://kbbi.co.id/daftar-kata?page="
    FILE_PATH = "assets/kata.txt"
    words = []
    for i in range(1, NUM_PAGE):
        print("page:", i)
        with urlopen(TEMPLATE_URL + str(i)) as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.find_all("a", {'href':re.compile(r'https://.*kbbi\.co\.id/arti-kata.*')}):
                words.append(anchor.text)
    f = open(FILE_PATH, "w")
    for word in words:
        f.write(word+'\n')
    f.close()

if __name__ == "__main__":    
    word_scraping()
