import json
import wikipedia
import requests
from bs4 import BeautifulSoup
import os
import urllib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import uuid
from tqdm import tqdm
from collections import Counter
import requests
import re
from dataclasses import dataclass

@dataclass
class Reference:
    author: str
    year: str
    title: str
    url: str

    def get_intext(self):
        return f'({self.author}, {self.year})'

    def validate(self):
        resp = requests.get(self.url)
        if resp.status_code // 100 == 2:
            return True
        return False

    def get_full_ref(self):
        root = urllib.parse.urlparse('https://docs.python.org/3/library/urllib.parse.html').hostname
        if root.count('.') > 1:
            root = '.'.join(root.split('.')[-2:])
            
        return f'{self.author}. ({self.year}). {self.title}. {root.capitalize()}. \n<a href={self.url}>{self.url}</a>'

stopwords = stopwords.words('english')



def clean(w):
    return ''.join([i for i in w if i.isalpha()])

class Data:
    def __init__(self, file, sources='sources.json'):
        with open(file, 'r', encoding="utf-8") as f:
            data = json.loads(f.read())

        with open(sources, 'r', encoding="utf-8") as f:
            sources = json.loads(f.read())

        self.data = {int(k): v for k, v in data.items()}
        self.sources = {k: Reference(**v) for k, v in sources.items()}
        all_ = []
        '''for source in self.sources:
            print(source)
            source = self.sources[source]
            print('\tIntext:', source.get_intext())
            print('\tLink is verified:', source.validate())
            print('\tFull ref:', source.get_full_ref())
            all_.append(source.get_full_ref())'''
        # all_.sort(key = lambda x: ord(x[0]))
        # print('\n\n'.join(all_))
        # for s in self.sources:
        #     if not self.sources[s].validate():
        #         print(self.sources[s].url)
        self.summaries = {}
        # self.add_wikipedia_defs()
        # self.add_images()

    def get_data(self, year):
        if year in self.data:
            images = []
            y = str(year)
            paths = [os.path.join('scaled_images', path) for path in os.listdir('scaled_images') if path.split('_')[0] == y]
            # if y in self.sources:
            #     return {'title': str(year) + ' A.D.', 'content': self.data[year] + self.sources.get_intext(), 'images': paths}
            # else:
            return {'title': str(year) + ' A.D.', 'content': self.data[year], 'images': paths}
        else:
            return {'title': str(year) + ' A.D.', 'content': 'Use the slider to navigate around the years, or use the Back and Next buttons to skip to events!', 'images': []}

    def add_wikipedia_defs(self):
        new_data = {}
        refined_list = [
            "SN 1572",
            "island of Hven",
            "Giordano Bruno",
            "Georg Wilhelm",
            "Wilhelm von Struve",
            "Giovanni Battista Donati",
            "radial velocities",
            "Ejnar Hertzsprung",
            "Hertzsprung-Russell diagram",
            "Henry Norris Russell",
            "spiral nebulae",
            "Vesto Melvin Slipher",
            "Cepheid variable star",
            "Clyde Tombaugh",
            "Karl Jansky",
            "Arno Penzias",
            "Cosmic Background Explorer",
            "Michel Mayor",
            "Didier Queloz",
            "51 Pegasi b",
            "dwarf planet Eris",
            "International Astronomical Union",
            "Transit of Venus",
            "New Horizons",
            "interstellar object",
            "galaxy M87",
            "Event Horizon Telescope"
        ]
        for key in tqdm(self.data):
            value = self.data[key]
            words = word_tokenize(value)
            copy_new = words.copy()
            inserted = []
            
            for width in range(3, 1, -1):
                for start_index in range(len(words) - width):
                    section = words[start_index: start_index + width]
                    if all([i.lower() in stopwords for i in section]):
                        continue

                    try:
                        title = ' '.join(section)
                        if title in refined_list:
                            res = wikipedia.summary(title, auto_suggest=False, redirect=True).strip()
                            self.summaries[title] = res
                            addition = len([i for i in inserted if i <= start_index])
                            copy_new.insert(start_index + width + addition, '</a>')
                            copy_new.insert(start_index + addition, f'''<a id="{clean(title) + '_' + str(uuid.uuid4())}">''')
                            inserted.append(start_index)
                            inserted.append(start_index + width)
                        # print(title, addition, inserted)
                        continue # skip one so we don't overlap words
                        
                        
                    except Exception as e:
                        pass # print('Error with title', title + ':', e)
            self.data[key] = ' '.join(copy_new)
                    

    def add_images(self):
        words = None
        image_data = {}
        for key in self.data:
            words_ = Counter([i for i in word_tokenize(self.data[key].lower()) if any([j.isalpha() for j in i])])
            if words:
                words += words_
            else:
                words = words_
        items = [t[0] for t in sorted(words.items(), key=lambda x: x[1])]

        for key in self.data:
            words_ = [i for i in word_tokenize(self.data[key].lower()) if any([j.isalpha() for j in i])]
            filtered_words = [word for word in words_ if word not in items[:10]]  # Removing top 10 most frequent words
            query = ' '.join(filtered_words)
            
            if not query:
                continue
            
            urls = get_image_urls(query)
            image_data[key] = []
            
            for idx, url in enumerate(urls):
                filename = f"{key}_{idx}.jpg"
                if download_image(url, filename):
                    image_data[key].append((url, filename))

        with open("image_data.json", "w") as file:
            json.dump(image_data, file, indent=4)
        
def get_image_urls(query, api_key='AIzaSyBv-XieS5VbBVj2wAemVnutMQUDC8TbRpU', search_engine_id='642b5ff7740d24213', num_results=10, start_index=1):
    """
    Fetch image URLs from Google Custom Search API.

    :param query: Search query string
    :param api_key: Google API key
    :param search_engine_id: Google Custom Search Engine ID (cx)
    :param num_results: Number of images to fetch (max 10 per request)
    :param start_index: Index of the first result (for pagination)
    :return: List of image URLs
    """
    url = (
        f"https://www.googleapis.com/customsearch/v1?"
        f"q={query}&cx={search_engine_id}&key={api_key}"
        f"&searchType=image&num={num_results}&start={start_index}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return []

    data = response.json()
    return [item["link"] for item in data.get("items", [])]

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return False


data = Data('data.json')
# data.add_images()
# updated = {str(k): v for k, v in data.data.items()}

'''import os
from PIL import Image
import imagehash
from nltk.tokenize import word_tokenize
import easyocr
reader = easyocr.Reader(['en'])


def load_and_compare(p1, p2):
    try:
        img1 = Image.open(p1).resize((128, 128), Image.Resampling.LANCZOS)
        img2 = Image.open(p2).resize((128, 128), Image.Resampling.LANCZOS)
    except:
        return {'PHASH': 100, 'DHASH': 100}
    phashes = imagehash.phash(img1), imagehash.phash(img2)
    dhashes = imagehash.dhash(img1), imagehash.dhash(img2)
    return {'PHASH': phashes[0] - phashes[1], 'DHASH': dhashes[0] - dhashes[1]}

hashes = []
current_year = 0
files = [i for i in os.listdir() if i.endswith('jpg')]
all_years = {}

for file in files:
    try:
        w, h = Image.open(file).size
        if w <= 300 or h < 300:
            print('Removing', file, 'because it\'s too low resolution')
            os.remove(file)
        try:
            text = reader.readtext(file, detail = 0)
            words = sum([len([j for j in word_tokenize(i) if len(j) > 1]) for i in text])
            if words > 20:
                print('Removing', file, 'because it\'s soooooo wordy')
                os.remove(file)

        except:
            pass

    except:
        try:
            os.remove(file)
            print('Removing', file, 'because it appears to be in an incorrect format')
        except:
            pass
files = [i for i in os.listdir() if i.endswith('jpg')]

for file in files:
    year = file.split('_')[0]
    if all_years.get(year, []):
        all_years[year].append(file)
    else:
        all_years[year] = [year]

from itertools import combinations
for year in all_years:
    for a, b in combinations(all_years[year], 2):
        if '.' not in a or '.' not in b:
            continue
        hashes = load_and_compare(a, b)
        # print(a, b, hashes)
        if hashes['PHASH'] < 15 or hashes['DHASH'] < 5:
            print('Removing', b, 'because it\'s too similar to', a)
            os.remove(b)'''

    

        
'''with open('wikilinks_added.json', 'w') as f:
    f.write(json.dumps(data.data, indent = 4))

with open('summaries.json', 'w') as f:
    f.write(json.dumps(data.summaries, indent = 4))'''

if __name__ == '__main__':
    import os
    from PIL import Image

    sizex, sizey = 400, 300

    for path in os.listdir('images'):
        file = Image.open(os.path.join('images', path))
        w, h = file.size
        if w <= sizex and h <= sizey:
            file.save(os.path.join('scaled_images', path))

        else:
            ratio = min(sizex/w, sizey/h)

            file.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS).save(os.path.join('scaled_images', path))

