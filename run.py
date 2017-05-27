import os
import pickle
import random
import subprocess

import settings
import tools

if __name__ == "__main__":
    if not os.path.exists("Messages/{}/Pretty/complete-pretty.json".format(settings.user_id)):
        subprocess.call("python FBMessageScraper/dumper.py {} 2000".format(settings.user_id).split())

    tools.get_conversation_history("Messages/{}/complete.json".format(settings.user_id), "DATA/raw_data.txt")
    tools.clean_input_text("DATA/raw_data.txt", "DATA/clean_data.txt")
    tools.generate_corpus("DATA/clean_data.txt", "DATA/corpus.p", settings.markov_length)
    corpus = pickle.load(open("DATA/corpus.p", 'rb'))

    text = "Theodore was not a violent man. In life, he wielded a calculator and a pen to work, a soft and steady voice at home, and in times of conflict, he mediated it with logic and reason. However, no amount of reason could've stopped the the bar fight at The Drunken Clam. Before he could even utter his fist word, a knife had been drawn and stabbed through his neck. And as he lay on the ground, the darkness encroaching, a fair maiden appeared with blinding light that cast away whatever shadows had dug themselves into the edges of his vision. Theodore, she said, her voice a nectar. I deem you worthy for the Palace of Kings. Then, the darkness took over."

    keywords = tools.get_keywords(text)
    react_message = tools.get_sentiment(text)
    keyword = tools.get_start_word(keywords, corpus)

    for _ in range(10):
        print tools.generate_markov_message(corpus, max_length=25)
