from keybert import KeyBERT

class KeyBERTWrapper():
    def __init__(self):
        self.kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    
    def predict(self, text):
        key_words = self.kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words=None)
        top_bigram = key_words[0][0]
        key_word_list = ", ".join([key_words[i][0] for i in range(len(key_words)) if i < 3])
        return top_bigram, key_word_list