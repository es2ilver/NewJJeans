import csv
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np
from konlpy.tag import Mecab

tokenizer = Mecab().nouns

def Preprocess(text):

    dictionary = pd.read_csv(filepath_or_buffer='ko_w2v_version2.txt', header=None, sep=" ", quoting=csv.QUOTE_NONE, usecols=[0]).values
    dictionary = [word[0] for word in dictionary]

    max_length_sentences = 20
    max_length_word = 32
    num_classes = 2

    document_encode = [
        [dictionary.index(word) if word in dictionary else -1 for word in
            tokenizer(sentences)] for sentences in sent_tokenize(text=text)
    ]

    for sentences in document_encode:
        if len(sentences) < max_length_word:
            extended_words = [-1 for _ in range(max_length_word - len(sentences))]
            sentences.extend(extended_words)
    if len(document_encode) < max_length_sentences:
        extended_sentences = [[-1 for _ in range(max_length_word)] for _ in
                              range(max_length_sentences - len(document_encode))]
        document_encode.extend(extended_sentences)

    document_encode = [sentences[:max_length_word] for sentences in document_encode][
                      :max_length_sentences]
    document_encode = np.stack(arrays=document_encode, axis=0)
    document_encode += 1
    
    empty_array = np.zeros_like(document_encode, dtype=np.int64)
    input_array = np.stack([document_encode, empty_array], axis=0)
    # if torch.cuda.is_available():
    #     feature = feature.cuda()
    
    return input_array
