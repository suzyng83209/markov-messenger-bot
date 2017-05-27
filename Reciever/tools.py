import ast
import json
import pickle
import random
import requests

from textblob import TextBlob
import nltk

import settings
import words

def get_conversation_history(data, outfile):
    """Scrapes json file and returns text file with only conversation history text

    Args:
        data: .json file with pretty json
        outfile: .txt file with beautified text
    """
    with open(data) as data_file:
        data = json.load(data_file)

    with open(outfile, 'wb') as f:
        for message in data:
            try:
                message = message['body'].encode("utf8")
            except:
                message = message['log_message_body'].encode("utf8")
            f.write("{} ".format(message))
    return


def clean_input_text(infile, outfile):
    """Takes in conversation history with another user and removes
    extraneous characters and typos.

    Args:
        infile: file with conversation history
        outfile: file with sanitized data
    """

    clean_infile = open(infile).read().replace('\n', ' ').replace("\"", "").lower()

    with open(outfile, 'wb') as f_out:
        f_out.write(clean_infile)


def generate_corpus(infile, outfile, length):
    """Takes in a text file and returns a dictionary that acts as a corpus
    to generate the Markov chain

    Args:
        infile: file with data to create corpus
        outfile: file to write corpus to
        length: how many words for a key in the corpus; can be 2 or 3
    """

    corpus = {}

    def generate_chain(words):
        if len(words) < length:
            return
        for i in range(len(words) - 2):
            yield (words[i], words[i+1], words[i+2])

    with open(infile, 'r') as f:
        for line in f.readlines():
            words = line.split()
            for word1, word2, word3 in generate_chain(words):
                key = (word1, word2)
                if key in corpus:
                    corpus[key].append(word3)
                else:
                    corpus[key] = [word3]

    pickle.dump(corpus, open("DATA/corpus.p", "wb" ))

    return corpus


def get_keywords(text):
    """Parses text and identifies keywords using NLTK

    Args:
        text: message to parse
    """
    sentences = nltk.sent_tokenize(text)
    unique_keywords = []
    keywords = []
    for sentence in sentences:
        words = nltk.pos_tag(nltk.word_tokenize(sentence))
        keywords += [word[0] for word in words if word[1] in ["NN", "NNP"]]

    for i in keywords:
        if i not in unique_keywords:
            unique_keywords.append(i)

    return unique_keywords


def get_start_word(keywords, corpus):
    """Compares message keywords with corpus to select best starting word

    Args:
        keywords: keywords
        corpus: corpus
    """

    matching_keywords = []
    for keyword in keywords:
        if keyword in [key[0] for key in corpus.keys()]:
            matching_keywords.append(keyword)

    if matching_keywords:
        return random.choice(matching_keywords)
    return None


def get_sentiment(text):
    """Performs sentiment analysis on text and returns a react

    Args:
        text: message to perform sentiment analysis on
    """
    negative_reacts = ["angry", "sad"]
    positive_reacts = ["wow", "haha", "love"]

    text = TextBlob(text)

    return text.sentiment.polarity

    if text.sentiment.polarity > 0:
        return random.choice(positive_reacts)
    elif text.sentiment.polarity <= 0:
        return random.choice(negative_reacts)


def generate_markov_message(corpus, start_word=None, sentence_type="statement", max_length=50):
    """Generates markov message based on keywords

    Args:
        corpus (dict): corpus to build markov chains off of
        start_word: first word for the markov chain
        sentence_type: type of sentence for markov chain
        max_length: maximum length of sentence
    """
    #Need to find way to relate keywords without it being the start word
    sword1 = random.choice(words.start_words[sentence_type])

    #Generate start words for markov chain
    attempts = 0
    while attempts < 5:
        attempts += 1
        try:
            sword2 = random.choice([key[1] for key in corpus.keys() if sword1 == key[0]])
            break
        except IndexError as e:
            continue


    if attempts == 5:
        sword1, sword2 = random.choice(corpus.keys())

    message = [sword1.capitalize(), sword2]

    #Generate sentence for markov chain
    while len(message) < max_length and (sword1, sword2) in corpus:
        if sword2.endswith(words.punctuation):
            break

        sword1, sword2 = sword2, random.choice(corpus[(sword1, sword2)])

        message.append(sword2)

    if sentence_type == "statement":
        return " ".join(message) + "."
    elif sentence_type == "question":
        return " ".join(message)[:-1] + "?"
        #TRAINING DATA IS TOO REFLECTIVE OF SENTENCES and not questions


# def send_message():
#
#
#
# def get_message():
