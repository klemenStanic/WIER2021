import nltk
from stop_words import stop_words_slovene
from nltk import word_tokenize
import bs4


def get_only_text_from_html(text):
    # Get text from html
    soup = bs4.BeautifulSoup(text, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace("\n", " ")

    return text


def remove_stopwords_and_lower_case(words):
    return [word.lower() for word in words if word not in stop_words_slovene]


def remove_punctuations(words):
    return [word for word in words if len(word) > 1]


def preprocess_text(text):
    text = get_only_text_from_html(text)

    out = dict()
    index = 0
    for word in text.split(" "):
        tokenized = word_tokenize(word)
        for token in tokenized:
            token = token.lower()
            if len(token) == 1 or token in stop_words_slovene:
                continue
            if token in out:
               out[token].append(index)
            else:
               out[token] = [index]
        index += 1

    return out

    # words = word_tokenize(text)
    # words = remove_stopwords_and_lower_case(words)
    # words = remove_punctuations(words)


def get_testing_text():
    with open("../data/evem.gov.si/evem.gov.si.1.html", "r") as f:
        text = f.read()
        return text


if __name__ == "__main__":
    nltk.data.path.append("../data/nltk_data")
    text = get_testing_text()
    preprocess_text(text)
