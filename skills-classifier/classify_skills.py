# for lemmatization
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
# import sys

# userInput = str(sys.argv[1])

# classifier model
import joblib
import spacy


def lemmantize_word(word):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)


def preprocess(word):
    word = word_tokenize(lemmantize_word(word.strip().lower()))
    processed_text = " ".join(word)
    return processed_text


# Load the trained model from the file
classifier = joblib.load("./models/skill_classifier_model.pkl")
vectorizer = joblib.load("./models/tfidf_vectorize.pkl")

# Load spaCy model for tokenization (not needed for new model)
nlp = spacy.load("en_core_web_sm")


# prediction model
def classify_skill(skill):
    """classifies the skill if it is hard (1) or soft skill (0)"""
    skill = [preprocess(skill)]
    input_skill_vector = vectorizer.transform(skill)

    # Use the loaded model for prediction
    prediction = classifier.predict(input_skill_vector)

    # Interpret the prediction (CHECK)
    # if skill.lower() == "advocacy":
    # if prediction[0] != 1:
    #     print(f"\n\n{new_skill} is a soft skill.")
    # else:
    #     print(f"\n\n{new_skill} is a hard skill.")

    return prediction[0]


# print('hard skill' if classify_skill(userInput) == 1 else 'soft skill')
