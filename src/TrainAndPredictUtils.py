from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords 
from sklearn.svm import SVC
from spacyParser import spacyParser
import string, pickle
spacy_parser = spacyParser().spacy_parser

# Create spacy tokenizer that parses a sentence and generates tokens
# these can also be replaced by word vectors 
def spacy_tokenizer(sentence):
    tokens = spacy_parser(sentence)
    tokens = [tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_ for tok in tokens]
    tokens = [tok for tok in tokens if (tok not in stopwords and tok not in string.punctuation)]
    return tokens

# Custom transformer using spaCy for transforming data
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        return [text.strip().lower() for text in X]
    def fit(self, X, y=None, **fit_params):
        return self
    def get_params(self, deep=True):
        return {}

# Gets the default pipeline for model fitting and predicting
def get_pipeline():
    vectorizer = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1)) 
    classifier = SVC(C=10, kernel='linear')

    pipe = Pipeline([("cleaner", predictors()),
                     ('vectorizer', vectorizer),
                     ('tfidftransformer', TfidfTransformer()),
                     ('classifier', classifier)])
    return pipe



# Ranker to filter entities using a pre-trained model
def filter_using_pretrained_model(entities, model_file):
    if len(entities) == 0:
        return entities
    try:
        with open(model_file, 'rb') as fid:
            model = pickle.load(fid)
    except:
        print("Could not read file:" + model_file)
        print("Encountered error: " + sys.exc_info()[0])

    X = list(entities)
    Yh = model.predict(X)
    return set([X[i] for i in range(len(X)) if Yh[i] == 'pos'])


