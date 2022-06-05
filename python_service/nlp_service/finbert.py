## Predict function is taken from https://github.com/ProsusAI/finBERT/blob/master/finbert/finbert.py

import sys
import nltk
nltk.download('punkt')
import pandas as pd
from nltk.tokenize import sent_tokenize
import numpy as np

from transformers import AutoTokenizer, AutoModelForSequenceClassification

sys.path.insert(1, './../../')
from python_service.nlp_service.utils import *


class FinBERT():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")


    def predict(self, text, batch_size=5):
        self.model.eval()
        sentences = sent_tokenize(text)
        label_list = ['positive', 'negative', 'neutral']
        label_dict = {0: 'positive', 1: 'negative', 2: 'neutral'}
        device = "cpu"
        result = pd.DataFrame(columns=['sentence', 'logit', 'prediction', 'sentiment_score'])
        for batch in chunks(sentences, batch_size):
            examples = [InputExample(str(i), sentence) for i, sentence in enumerate(batch)]
            features = convert_examples_to_features(examples, label_list, 64, self.tokenizer)

            all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long).to(device)
            all_attention_mask = torch.tensor([f.attention_mask for f in features], dtype=torch.long).to(device)
            all_token_type_ids = torch.tensor([f.token_type_ids for f in features], dtype=torch.long).to(device)

            with torch.no_grad():
                model  = self.model.to(device)

                logits = model(all_input_ids, all_attention_mask, all_token_type_ids)[0]
                #logging.info(logits)
                logits = softmax(np.array(logits.cpu()))
                sentiment_score = pd.Series(logits[:, 0] - logits[:, 1])
                predictions = np.squeeze(np.argmax(logits, axis=1))

                batch_result = {'sentence': batch,
                                'logit': list(logits),
                                'prediction': predictions,
                                'sentiment_score': sentiment_score}

                batch_result = pd.DataFrame(batch_result)
                result = pd.concat([result, batch_result], ignore_index=True)

        result['prediction'] = result.prediction.apply(lambda x: label_dict[x])
        
        return result