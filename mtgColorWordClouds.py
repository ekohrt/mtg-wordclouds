# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 08:57:18 2021

@author: ekohrt

Reference: https://towardsdatascience.com/simple-wordcloud-in-python-2ae54a9f58e5
Filling a shape: https://towardsdatascience.com/how-to-create-beautiful-word-clouds-in-python-cfcf85141214
"""

import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from string import punctuation as PUNCT
import numpy as np
from PIL import Image



WHITE = 'W'
RED = 'R'
GREEN = 'G'
BLUE = 'U'
BLACK = 'B'

white_mask = np.array(Image.open('mana_symbol_masks/mana_symbol_w_lg.png'))
red_mask   = np.array(Image.open('mana_symbol_masks/mana_symbol_r_lg.png'))
green_mask = np.array(Image.open('mana_symbol_masks/mana_symbol_g_lg.png'))
blue_mask  = np.array(Image.open('mana_symbol_masks/mana_symbol_u_lg.png'))
black_mask = np.array(Image.open('mana_symbol_masks/mana_symbol_b_lg.png'))

#Wordcloud color schemes for each mtg color 
#List of all colormaps: https://matplotlib.org/stable/tutorials/colors/colormaps.html
COLOR_SCHEMES = {WHITE: {'bkg': (241, 240, 233), 'scheme': 'Wistia',  'mask': white_mask}, #(241, 240, 233)
                 RED:   {'bkg': (243, 210, 195), 'scheme': 'Reds',    'mask': red_mask}, #(243, 210, 195)
                 GREEN: {'bkg': (194, 209, 202), 'scheme': 'Greens',  'mask': green_mask}, #(194, 209, 202)
                 BLUE:  {'bkg': (199, 227, 241), 'scheme': 'Blues',    'mask': blue_mask}, #(199, 227, 241) #'cool', 'BuPu', 'Blues', 'coolwarm'
                 BLACK: {'bkg': (189, 183, 183), 'scheme': 'Purples', 'mask': black_mask}} #(189, 183, 183)
                
myStopWords = {"a","an","and","and/or","are","as","at","be","by","could","dont",
                 "for","if","in","is","it","its","may","of","on","or","put","that","thats",
                 "the","their","them","then","they","this","those","to","was","where",
                 "with","you","your","—",
                 #extra stop words that appear in each color often
                 "cast", "whenever", "target", "creature", "creatures", "card", "cards", "spell", 
                 "opponent", "player", "control", "battlefield", "turn", "end", 
                 "U", "G", "B", "R", "W", 'get', 'gets', 'gain', 'gains'}

with open('AtomicCards_Small.json', encoding='utf-8') as json_file:
    cards_dict = json.load(json_file)
    




"""
Creates a rectangular word cloud in the console for the given color
"""
def make_normal_word_cloud(color_char):
    #get combined text from all cards of given color
    text = collect_all_text_for_color(color_char)
    
    #plot the wordcloud
    bkg_color = COLOR_SCHEMES[color_char]['bkg']
    color_scheme = COLOR_SCHEMES[color_char]['scheme']
    
    # Generate word cloud
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, 
                          background_color=bkg_color, colormap=color_scheme, 
                          collocations=False, stopwords = STOPWORDS|myStopWords).generate(text)
    #display in console
    plot_cloud(wordcloud)
    
    
    
"""
Creates a mana-symbol-shaped word cloud in the console for a given color
"""
def make_shaped_word_cloud(color_char):
    #get combined text from all cards of given color
    text = collect_all_text_for_color(color_char)
    
    #plot the wordcloud
    bkg_color = 'black' #COLOR_SCHEMES[color_char]['bkg']
    color_scheme = COLOR_SCHEMES[color_char]['scheme']
    mask = COLOR_SCHEMES[color_char]['mask']
    
    # Generate word cloud
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, 
                          background_color=bkg_color, colormap=color_scheme, 
                          collocations=False, stopwords = STOPWORDS|myStopWords,
                          mask=mask, contour_color='black', contour_width=1).generate(text)
    #display in console
    plot_cloud(wordcloud)





"""
Helper - Loops over all MtG cards of the given color and adds their text
@param color_char is 'W', 'B', 'U', 'R', or 'G'
"""
def collect_all_text_for_color(color_char):
    # get all the card text and mash it together
    corpus = []
    for cardname in cards_dict['data']:
        entry = cards_dict['data'][cardname]
        #check all faces of the card: if it's the right color, collect its text
        for face in entry:
            if color_char in face.get('colors', []):
                card_text = face.get('text', "")
                corpus.append(card_text)
    text = " ".join(corpus)
    
    #clean the text: remove punctuation
    text.translate(str.maketrans('', '', PUNCT))
    return text


"""
Helper - display wordcloud object in console
"""
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off")




    
def main():
    # use GREEN, BLACK, BLUE, RED, or WHITE
    make_shaped_word_cloud(WHITE)
    # make_shaped_word_cloud(RED)
    # make_shaped_word_cloud(GREEN)
    # make_shaped_word_cloud(BLACK)
    # make_shaped_word_cloud(BLUE)
    
    
if __name__ == "__main__":
    main()