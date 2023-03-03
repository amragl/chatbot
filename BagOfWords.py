import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

######################################################
#  Getting data from txt file for similarity
#######################################################

f = open('test.txt', 'r')
raw = f.read()
raw = raw.lower()

#nltk.download('punkt')  # download libraries on first time use
#nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)  # converts data to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of word_tokens

# WordNet is a semantically-oriented dictionary of English included in nltk
lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


def LemNormalize(text):
        for p in string.punctuation:
            text = text.replace(p, '')
        return LemTokens(nltk.word_tokenize(text.lower()))


# generating a response
def response(user_response):
    robo_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    print (req_tfidf)
    if(req_tfidf == 0):
        robo_response = robo_response+"Joe similarity:I am sorry! There isn't anything similar in the system. Could you ask differently?"
        return robo_response
    else:
        robo_response = robo_response+("Joe similarity:  Does this answer your question? -> ")
        if len(sent_tokens[idx].split(",")) > 1:
            answer = sent_tokens[idx].split(",",1)[1]
        else:
            answer = sent_tokens[idx]
        robo_response = robo_response+answer
        return robo_response

#######################################################
#  End of Similarity Section
#######################################################



def bag_of_words(userInput):
    global word_tokens
    flag = True
    while (flag == True):
        user_response = userInput
        user_response = user_response.lower()
        if (user_response != 'bye'):
            sent_tokens.append(user_response)
            word_tokens = word_tokens + nltk.word_tokenize(user_response)
            final_words = list(set(word_tokens))
            print(" cmd99 Joe: ")
            print(response(user_response))
            sent_tokens.remove(user_response)
            flag = False
        else:
            flag = False
            print("Joe: Bye! take care..")
