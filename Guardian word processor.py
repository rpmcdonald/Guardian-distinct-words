import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
nlp = spacy.load('en')
nlp.max_length = 1198623

# Set up BeautifulSoup for the front page to get the url for each article saving them into coverpage_news
r1 = requests.get(url='https://www.theguardian.com/uk')
coverpage = r1.content
soup1 = BeautifulSoup(coverpage, 'html5lib')
coverpage_news = soup1.find_all('a', class_='u-faux-block-link__overlay js-headline-text')

# Set up empty variable to store the text from each paragraph
compiled_text = []
for article in coverpage_news:
    # Similar process to above, using BeautifulSoup to get the text of each paragraph in the article
    r2 = requests.get(url=article['href'])
    article_page = r2.content
    soup2 = BeautifulSoup(article_page, 'html5lib')
    article_text = soup2.find_all('p')
    # Use del to delete the authors and time posted but retain headline
    del article_text[1:3]
    for paragraph in article_text:
        # Using a try/except incase the program runs into something it doesn't understand and I have not predicted
        try:
            # Some live text pages begin paragraphs with the time or a space allowing me to remove them
            if paragraph.get_text()[0] not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ' ', '\n'):
                compiled_text.append(paragraph.get_text())
        except:
            pass

# Compiles the list of paragraphs into one big text
text = ' '.join(compiled_text)

# Breaks the text into tokens and removes most symbols
# Can also use token.text.lower() if I don't want to consider upper and lower case to be different,
# this may effect businesses though. Perhaps I can just remove capitalisation of each sentence?
tokens = [token.text for token in nlp(text) if
                token.text not in '\n\n \n\n\n!"-#$%&()--.*+,-/:;<=>?@{\\}^_`{|}~\t\n ...']

# Removes stray tokens which begin with . or '
tokens = [token for token in tokens if
          token[0] not in '.\'/0123456789']

# Number of articles
len(coverpage_news)

# The total word list sorted alphabetical, number of total words, list of different words sorted alphabetically and
# number of different words
words = sorted(tokens)
words_len = len(tokens)
unique_words = sorted(set(tokens))
unique_words_len = len(set(tokens))

# Dictionary of words with counts e.g. {'The': 12}
word_dict = {}

# Make lists by letter to better iterate and speed up the process
a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = \
    ['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], \
    ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z']
lowercase = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z]
A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = \
    ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], \
    ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']
uppercase = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z]

# Goes through each letter upper and lowercase counting them and removing the value as to save time not reiterating
for i in words:
    for letter in lowercase:
        if letter[0] == i[0]:
            letter.append(i)
            words.remove(i)
for i in words:
    for letter in uppercase:
        if letter[0] == i[0]:
            letter.append(i)
            words.remove(i)

for letter in lowercase:
    del letter[0]
for letter in uppercase:
    del letter[0]

# Adds the word and value into the dictionary
for letter in lowercase:
    for word in letter:
        word_dict[word] = letter.count(word)
for letter in uppercase:
    for word in letter:
        word_dict[word] = letter.count(word)

# Output all the information into a database
df = pd.DataFrame.from_dict(orient='index', data=word_dict, columns=['Count'])
