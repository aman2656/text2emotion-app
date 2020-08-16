# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import pandas as pd
import numpy as np
from functions import *
import matplotlib.pyplot as plt


cols = ['c','m','r','b', 'g']
labels=['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']

st.title('Emotion Analyzer')
sentence = st.text_area('Input your sentence here:')
if st.button("submit"):
    if sentence:
        emotions = get_emotion(sentence)
        st.write(emotions)
        plt.pie(list(emotions.values()),
                labels=labels,
                colors=cols,
                startangle=90,
                autopct='%1.1f%%')
        if sum(list(emotions.values())) is not 0:
            st.pyplot()
