# from sentence_transformers import SentenceTransformer
from underthesea import word_tokenize
import re
import random
import string
# from configs.index import stop_word

import json

def stop_word():
    stopwords_file = "public/stopword.txt"
    with open(stopwords_file, "r", encoding="utf-8") as f:
        stopwords = [line.strip() for line in f]
    return stopwords

list_stop_words = stop_word()

# model = SentenceTransformer('bkai-foundation-models/vietnamese-bi-encoder')

def slugify(input_string):
    cleaned_string = str(input_string).lower()
    cleaned_string = re.sub(r'`|~|!|@|#|\||\$|%|\^|&|\*|\(|\)|\+|=|,|\.|\/|\?|>|<|\'|"|:|;|_/', '', cleaned_string)
    cleaned_string = re.sub(r'@-|-@|@', '', cleaned_string)
    return cleaned_string

def generate_random_string(length, allowed_chars=None):
    possible_chars = allowed_chars or string.ascii_letters + string.digits
    random_string = ''.join(random.choice(possible_chars) for _ in range(length))
    return random_string

# def convert_text_to_vector(text):
#     segment_text = word_tokenize(sentence=text, format='text').lower()
#     result = model.encode(segment_text).tolist()
#     return result

def normalize_text(text):
    segment_text = word_tokenize(sentence=slugify(text), format='text')
    arr_segment_text = segment_text.split()
    filtered_words = [word for word in arr_segment_text if word not in list_stop_words]
    filtered_string = ' '.join(filtered_words)
    return filtered_string

