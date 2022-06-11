import csv
import sys
import ast
import re
import math
from collections import defaultdict
import pyphen

csv.field_size_limit(sys.maxsize)

def rubrikParse(rubrik):
    rubrik = re.sub("[\[\]\']", "", rubrik)
    rubrik = rubrik.split(", ")
    if len(rubrik) > 1:
        for item in rubrik:
            if not "/" in item:
                return item
                break
    else:
        return rubrik[0]

def parseFile(dataTuple):
    parsedData = []
    fileName, idCol, wordCountCol, rubrikCol, bodyCol = dataTuple
    with open(fileName,"r") as data:
        reader = csv.reader(data)
        next(reader)
        for row in reader:
            if len(row[rubrikCol]) > 0 and not int(row[wordCountCol]) == 0:
                parsedData.append((
                    row[idCol],
                    int(row[wordCountCol]),
                    rubrikParse(row[rubrikCol]),
                    row[bodyCol]
                ))
    return parsedData


def article_score(article):
    # Prepare UWC Calculation
    with open("common_words.txt", "r") as file:
        common_words = file.readline().split(", ")
        common_words[-1][:-1]

    body = re.sub('[^a-zA-ZöüäÖÄÜß\- ]', '', article[3]).lower()
    body_split = body.split(" ")
    unique_split = list(set(body_split))
    no_common_words = [i for i in unique_split if i not in common_words]

    # Calculate score
    uwc = len(no_common_words)
    score = float(int(uwc/article[1]*10000))/100
    return [uwc,score]

# Count Syllables
def count_sylls_german(text):
    dic = pyphen.Pyphen(lang='de_DE')

    text = re.sub("[^a-zA-ZäöüÄÖÜß ]", " ", text)
    text = re.sub("\s+", " ", text)

    num_of_sylls = 0
    sylls_per_word = defaultdict(int)
    chars_per_word = defaultdict(int)
    for word in text.split(" "):
        syll_counter = 0
        sylls = dic.inserted(word)
        syll_counter += (1 + sylls.count("-"))
        num_of_sylls += syll_counter
        sylls_per_word[syll_counter] += 1
        chars_per_word[len(word)] += 1

    return num_of_sylls, sylls_per_word, chars_per_word

# Count German Sentences in text
def count_sentences_german(text):
    """ Count number of sentences by counting terminals but avoid counting abbreviations """
    # Removes punctuation except terminals of sentences
    text = re.sub("[^a-zA-ZäöüÄÖÜß\.!? ]", " ", text)
    # Identifies the last four characters of a sentence
    return len(re.findall("[a-zäöüß)]{3}[\.?!][\n\s]", text)) + 1

def wiener_sachtext_formel(text):
    # Setup Text params
    number_of_words = text.count(" ") + 1
    number_of_sentences = count_sentences_german(text)
    number_of_sylls, sylls_per_word, chars_per_word = count_sylls_german(text)
    avg_sentence_length = number_of_words / number_of_sentences
    avg_syllables = number_of_sylls / number_of_words

    # Count Words that are particularly long
    num_long_words = sum([v for k, v in sylls_per_word.items() if k >= 3])
    ratio_lw = num_long_words / number_of_words

    num_very_long_words = sum([v for k, v in chars_per_word.items() if k >= 6])
    ratio_vlw = num_very_long_words / number_of_words

    avg_syll = sylls_per_word[1] / number_of_words

    wsf = calc_wsf(
        ratio_lw,
        avg_sentence_length,
        ratio_vlw,
        avg_syll
    )
    wsf = float(int(wsf*100)) / 100
    return wsf

def calc_wsf(ms, sl, iw, es):
    """
    MS: Prozentanteil der Wörter mit drei oder mehr Silben,
    SL: mittlere Satzlänge (Anzahl Wörter),
    IW: Prozentanteil der Wörter mit mehr als sechs Buchstaben,
    ES: Prozentanteil der einsilbigen Wörter.
    """
    wsf = 19.35 * ms + 0.1672 * sl + 12.97 * iw - 3.27 * es - 0.875
    return wsf

def write_csv(data):
    with open(use[0][:-4] + "_out.csv","w+") as file:
        writer = csv.writer(file,delimiter=',')
        writer.writerows(data)

def calculate_scores(parsedData):
    article_scores = []
    for article in parsedData:
        uwc, our_score = article_score(article)
        wiener_score = wiener_sachtext_formel(article[3])

        if wiener_score > 12 and our_score < 1.5:
            print(article[3])

        article_scores.append([
            article[2],
            article[1],
            uwc,
            our_score,
            wiener_score
        ])
    return article_scores

use_goethe = ("goethe.csv", 0, 2, 1, 3)
use_cxense = ("cxense.csv", 4, 2, 11, 5)

use = use_cxense

parsed = parseFile(use)
calculated = calculate_scores(parsed)
write_csv(calculated)
