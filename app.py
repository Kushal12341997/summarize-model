import re
import spacy
import math
from flask import Flask, request

app = Flask(__name__)

eng_model = spacy.load('en_core_web_sm')
stop_words = eng_model.Defaults.stop_words


@app.route('/model/summarize', methods=['POST'])
def summarize_text():
    print("Received text to be summarized")
    text_data = request.json["text"]
    # TOKENIZING THE TEXT DATA
    list_of_sentences = text_data.split('.')
    list_of_words = []
    for sentence in list_of_sentences:
        for word in sentence.split(' '):
            if word not in stop_words and str.isalnum(word):
                list_of_words.append(re.sub('[^A-Za-z0-9]+', '', word))
    # print("Tokenized Data :: ", list_of_words)

    # COMPUTING WEIGHTED FREQUENCY OF WORDS
    weighted_frequency = {}
    max_frequency = 0
    for word in list_of_words:
        if word not in weighted_frequency:
            count_of_word = list_of_words.count(word)
            weighted_frequency[word] = count_of_word
            if count_of_word > max_frequency:
                max_frequency = count_of_word
    for key, value in weighted_frequency.copy().items():
        weighted_frequency[key] = value / max_frequency

    sentence_score_mapping = {}
    for sentence in list_of_sentences:
        sentence_score_mapping[sentence] = 0
        for word in sentence.split(' '):
            if re.sub('[^A-Za-z0-9]+', '', word) in weighted_frequency:
                sentence_score_mapping[sentence] += weighted_frequency[re.sub('[^A-Za-z0-9]+', '', word)]

    sentence_score_mapping = sorted(sentence_score_mapping.items(), key=lambda mapping: mapping[1])
    sentence_score_mapping.reverse()

    # KEEPING 40% of the sentences
    sentences_to_keep = math.ceil(len(sentence_score_mapping) * 0.8)
    del sentence_score_mapping[-sentences_to_keep:]
    # print("Sentence score mapping :: ", sentence_score_mapping)

    summarized_text = ""
    for sentence in list_of_sentences:
        if sentence in (item[0] for item in sentence_score_mapping):
            summarized_text += sentence + ". "
    return summarized_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
