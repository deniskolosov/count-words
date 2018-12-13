# download stopwords corpus, you need to run it once
import nltk
nltk.download("stopwords")

import os
import click

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from bs4 import BeautifulSoup
from collections import Counter

# Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian")


# Preprocess function
def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)

    return text

@click.command()
@click.argument('directory')
def main(directory):
    path = directory
    filenames = [f for f in os.listdir(path) if "message" in f]
    words = []
    for name in filenames:
        html_doc = open(path + name, 'r').read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        res = '  '.join([s.text.strip() for s in soup.find_all('div', {'class': 'text'})])
        words.extend(preprocess_text(res).split())
    c = Counter(words)
    c.most_common(20)
    click.echo("Наиболее употребляемые слова: ")
    for pair in c.most_common(20):
        print("{}: {}".format(pair[0], pair[1]))


if __name__ == "__main__":
    main()
