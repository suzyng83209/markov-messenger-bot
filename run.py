import pickle
import random

import settings
import tools

if __name__ == "__main__":
    tools.clean_input_text("DATA/raw_data.txt", "DATA/clean_data.txt")
    tools.generate_corpus("DATA/clean_data.txt", "DATA/corpus.p", settings.markov_length)

    corpus = pickle.load(open("DATA/corpus.p", 'rb'))

    for x in range(100):
        print tools.generate_markov_message(corpus, sentence_type="question")
