import json

def stop_word():
    stopwords_file = "public/stopword.txt"
    with open(stopwords_file, "r", encoding="utf-8") as f:
        stopwords = [line.strip() for line in f]
    return stopwords
