#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Load the Naive Bayes model parameters and classifies/predicts labels for input data

import json
from math import log
import sys
from utils import *

# parse command-line params
if len(sys.argv) != 2:
    print "Usage: python nbclassify.py /path/to/text/file"
    exit(1)


# load Naive Bayes Model parameters
with open('nbmodel.txt', 'rb') as f_nb_params:
    json_prob = json.load(f_nb_params)
# print json_prob
prior_prob = json_prob["prior"]
posterior_prob = json_prob["posterior"]
# print posterior_prob


# Predict veracity and sentiment of review
def classify_text(rev_text):
    # In our calculations, it's imperative to use LOG so that we don't suffer from underflows
    p_k_given_text = {  # init val
        "truthful": log(prior_prob["truthful"]),
        "deceptive": log(prior_prob["deceptive"]),
        "positive": log(prior_prob["positive"]),
        "negative": log(prior_prob["negative"])
    }

    for word in rev_text.translate(translation_table, "'").split():  # delete ' character
        # for each word in the text description of a review
        word_length = len(word)

        if word_length > 2:  # only consider words with more than 2 characters
            if word_length == 3:  # ignore most common frequent 3-letter words in English that are not helpful - taken from Cryptography
                if word in li_freq_words:
                    continue

            if word in posterior_prob:  # only consider known tokens; ignore unknown tokens
                for k in rev_classes:
                    p_k_given_text[k] += log(posterior_prob[word][k])

    # print p_k_given_text
    predict_veracity = "truthful" if p_k_given_text["truthful"] > p_k_given_text["deceptive"] else "deceptive"
    predict_sentiment = "positive" if p_k_given_text["positive"] > p_k_given_text["negative"] else "negative"

    return (predict_veracity, predict_sentiment)



# Open test file which contains reviews (id + text) and classify them
test_file_text = sys.argv[1]
f_out = open('nboutput.txt', 'wb') # file to write output

with open(test_file_text) as f_text:
    for line_ftext in f_text:
        # Get id and text. Make text lowercase
        rev_id, rev_text = line_ftext.strip().split(' ', 1)
        (predict_veracity, predict_sentiment) = classify_text(rev_text)
        f_out.write("%s %s %s\n" %(rev_id, predict_veracity, predict_sentiment))
        # f_out.write("%s %s\n" %(predict_veracity, predict_sentiment))
f_out.close()

