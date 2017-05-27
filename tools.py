
import pickle
import random

import words

def clean_input_text(infile, outfile):
    """Takes in conversation history with another user and removes
    extraneous characters

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


def generate_markov_message(corpus, keywords=None, sentence_type="statement", max_length=50):
    """Generates markov message based on keywords"""

    #Generate start words for markov chain
    while True:
        try:
            sword1 = random.choice(words.start_words[sentence_type])
            sword2 = random.choice([key[1] for key in corpus.keys() if sword1 == key[0]])
            break
        except IndexError as e:
            continue

    message = [sword1.capitalize(), sword2]

    #Generate sentence for markov chain
    while len(message) < max_length and (sword1, sword2) in corpus:
        if sword2.endswith(words.punctuation):
            break

        sword1, sword2 = sword2, random.choice(corpus[(sword1, sword2)])

        message.append(sword2)

    if sentence_type == "statement":
        return " ".join(message)[:-1] + "."
    elif sentence_type == "question":
        return " ".join(message)[:-1] + "?"
        #TRAINING DATA IS TOO REFLECTIVE OF SENTENCES and not questions