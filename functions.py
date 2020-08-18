import pandas as pd
from matplotlib import pyplot as plt
import nltk
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
import streamlit as st
import emoji
from emot.emo_unicode import UNICODE_EMO, EMOTICONS

def removing_shortcuts(text):
    full_words = []
    shortcuts = {'u': 'you', 'y': 'why', 'r': 'are', 'doin': 'doing', 'hw': 'how', 'k': 'okay', 'm': 'am',
                 'b4': 'before',
                 'idc': "i do not care", 'ty': 'thank you', 'wlcm': 'welcome', 'bc': 'because', '<3': 'love',
                 'xoxo': 'love',
                 'ttyl': 'talk to you later', 'gr8': 'great', 'bday': 'birthday', 'awsm': 'awesome', 'gud': 'good',
                 'h8': 'hate',
                 'lv': 'love', 'dm': 'direct message', 'rt': 'retweet', 'wtf': 'hate', 'idgaf': 'hate',
                 'irl': 'in real life', 'yolo': 'you only live once', "don't": "do not", 'g8': 'great',
                 "won't": "will not", 'tbh': 'to be honest', 'caj': 'casual', 'Ikr': 'I know, right?',
                 'omw': 'on my way',
                 'ofc': 'of course', 'Idc': "I don't care", 'Irl': 'In real life', 'tbf': 'To be fair',
                 'obvs': 'obviously', 'v': 'very', 'atm': 'at the moment',
                 'col': 'crying out loud', 'gbu': 'god bless you', 'gby': 'god bless you', 'gotcha': 'I got you',
                 'hehe': 'laughing', 'haha': 'laughing', 'hf': 'have fun',
                 'hry': 'hurry', 'hw': 'hardwork', 'idc': 'i don’t care', 'ikr': 'i know right', 'k': 'ok',
                 'lmao': 'laughing my ass off', 'lol': 'laughing out loud',
                 'n1': 'nice one', 'na': 'not available', 'qt': 'cutie', 'qtpi': 'cutie pie', 'rip': 'rest in peace',
                 'sry': 'sorry', 'tc': 'take care',
                 'thnks': 'thanks', 'thx': 'thanks', 'thnk': 'thanks', 'ttyl': 'talk to you later', 'txt': 'text',
                 'ugh': 'disgusted', 'w8': 'wait', "not sad": "happy"}

    for token in text:
        if token in shortcuts.keys():
            token = shortcuts[token]
        full_words.append(token)
    text = " ".join(full_words)
    return text


def removing_stopwords(text):
    stop_words = set(stopwords.words('english'))
    stop = [x.lower() for x in stop_words]
    return [word for word in text if not word in stopwords.words()]


def lemmatization(words_big):
    lemma = WordNetLemmatizer()
    stemmed_words = [lemma.lemmatize(word, 'v') for word in words_big]
    stemmed_words = [lemma.lemmatize(word, 'n') for word in stemmed_words]
    return " ".join(stemmed_words)

def removing_not(text):
    d = {'not sad': 'Happy', 'not bad': 'Happy', 'not boring': 'Happy', 'not wrong': 'Happy',
         'not bored': 'Happy', 'not jealous': 'Happy', 'not happy': 'Sad', 'not well': 'Sad',
         'not suitable': 'Angry', 'not right': 'Angry', 'not good': 'Sad', 'not excited': 'Angry',
         'not funny ': 'Sad', 'not  kind': 'Sad', 'not proud': 'Angry', 'not cool': 'Angry',
         'not funny': 'Angry', 'not kind': 'Angry', 'not open': 'Angry', 'not safe': 'Fear',
         'not enough': 'Empty', "not know": "Unknown"}
    f = re.findall("not\s\w+", text)
    for i in f:
        try:
            text = text.replace(i, d[i])
        except:
            pass
    text = text.lower()
    return text

def removing_contradictions(text):
    if text.count("n't"):
        text = text.replace("n't", " not")
    text = re.sub("ai\snot", "am not", text)
    text = re.sub("wo\snot", "will not", text)
    return text

def emojis_extractor(text):
    emoj = pd.read_csv("Emoji.csv")
    a = " ".join(c for c in text if c in emoji.UNICODE_EMOJI).split()
    for i in a:
        try:
            text = text.replace(i, " "+emoj['Emotion'][list(emoj["Emojis"]).index(i)]+" ")
        except:
            pass
    return text.lower()

def cleaning(text):
    text = text.lower()
    text = emojis_extractor(text)
    text = re.sub(r'http\S+|www.\S+', '', text)
    text = removing_contradictions(text)
    text = removing_not(text)
    text = text.split()
    text = removing_shortcuts(text)
    text = ' '.join([i for i in text.split() if not i.isdigit()])
    text = word_tokenize(text)
    words_alpha = removing_stopwords(text)
    words_big = [word for word in words_alpha if len(word) > 2]
    clean_text = lemmatization(words_big)
    clean_text = clean_text.replace('   ', ' ')
    clean_text = clean_text.replace('  ', ' ')
    # print(clean_text)
    return clean_text

@st.cache
def get_emotion(input):
  df = pd.read_csv('_Emotions.csv')
  text = cleaning(input).split()
  emotion_values=[]
  emotions = {"Happy":0, "Angry":0, "Surprise":0, "Sad":0, "Fear":0}
  y=0
  try:
    for i in text:
      try:
        a = list(df['Words']).index(i)
        if a:
          emotions[df['Emotion'][a]]+=1
      except:
        pass
    if sum(emotions.values()) is 0:
      return emotions
    for i in emotions:
      emotion_values.append(round((emotions[i]/sum(emotions.values())),2))
    for j in emotions:
      emotions[j] = emotion_values[y]
      y+=1
    return emotions
  except:
    pass
