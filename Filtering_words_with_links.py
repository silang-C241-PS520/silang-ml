from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests

def word_scraping_kbbi():
    TEMPLATE_URL = "https://kbbi.co.id/daftar-kata?page="
    words = []
    for i in range(1, 108):  # Total 107 pages
        print("Scraping KBBI page:", i)
        with urlopen(TEMPLATE_URL + str(i)) as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.find_all("a", {'href': re.compile(r'https://.*kbbi\.co\.id/arti-kata.*')}):
                word = anchor.text.strip()
                words.append(word)
    return words

def word_scraping_pmpk():
    URL = "https://pmpk.kemdikbud.go.id/sibi/SIBI/katadasar/"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    words = []
    for td in soup.find_all("td"):
        word = td.text.strip()
        words.append(word)
    return words

def find_common_words_and_generate_links(words_kbbi, words_pmpk):
    # Extract the names without extension from PMPK words for comparison
    stripped_words_pmpk = [word.replace('.webm', '') for word in words_pmpk]
    common_words = set(words_kbbi).intersection(set(stripped_words_pmpk))
    print(f"Found {len(common_words)} common words.")
    video_links = {}
    for word in common_words:
        video_link = f"https://pmpk.kemdikbud.go.id/sibi/SIBI/katadasar/{word}.webm"
        video_links[word] = video_link
    return video_links

if __name__ == "__main__":
    #words_kbbi = word_scraping_kbbi()
    #print(f"Scraped words from KBBI: {len(words_kbbi)} words")
    
    words_pmpk = word_scraping_pmpk()
    print(f"Scraped words from PMPK Kemdikbud: {len(words_pmpk)} words")

    f = open('assets/new_common_words.txt')
    words_kbbi = []
    for line in f:
        word = line.strip()
        words_kbbi.append(word)

    f.close()
    
    video_links = find_common_words_and_generate_links(words_kbbi, words_pmpk)

    with open("common_words_with_videos.txt", "w") as f:
        for word, link in video_links.items():
            f.write(f"{word}: {link}\n")

    print("Scraping completed. Check common_words_with_videos.txt for results.")
