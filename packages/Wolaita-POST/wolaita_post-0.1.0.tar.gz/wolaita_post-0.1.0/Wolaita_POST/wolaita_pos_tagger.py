import pickle
import numpy as np
import tensorflow as tf
from nltk import word_tokenize
from keras.preprocessing.sequence import pad_sequences
from gensim.models import KeyedVectors

# Constants
MAX_SEQ_LENGTH = 91

class WolaitaPOSTagger:
    def __init__(self, model_path, word_vector_path, word_tokenizer_path, tag_tokenizer_path):
        self.model = tf.keras.models.load_model(model_path)
        self.word_vectors = KeyedVectors.load_word2vec_format(word_vector_path, binary=True, encoding='latin1')
        self.word_tokenizer = self._load_pickle(word_tokenizer_path)
        self.tag_tokenizer = self._load_pickle(tag_tokenizer_path)
        self.reverse_word_index = {v: k for k, v in self.word_tokenizer.word_index.items()}
        self.reverse_tag_index = {v: k for k, v in self.tag_tokenizer.word_index.items()}

    def _load_pickle(self, file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    def predict_tags(self, sentence):
        if not sentence.strip():
            return "Error: Please enter a valid sentence."

        tokenized_sentence = word_tokenize(sentence)
        encoded_sentence = [self.word_tokenizer.word_index.get(word, 0) for word in tokenized_sentence]
        X_Samp = pad_sequences([encoded_sentence], maxlen=MAX_SEQ_LENGTH, padding="post", value=0)
        p = self.model.predict(X_Samp)
        p = np.argmax(p, axis=-1)

        results = []
        for w, pred in zip(X_Samp[0], p[0]):
            if w != 0:
                word = self.reverse_word_index.get(w, "UNK")
                tag = self.reverse_tag_index.get(pred, "UNK")
                results.append((word, tag))

        return results
