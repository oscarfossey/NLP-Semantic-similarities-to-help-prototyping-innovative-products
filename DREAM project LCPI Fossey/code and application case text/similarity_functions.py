# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:12:16 2021

@author: Oscar Fossey

This code has to be linked we the paper of Oscar Fossey Design Rules Extractor for Additive Manufacturability (DREAM)
"""

"""
This module define all the NLP functions/method we will use in the DREAM tool

"""

"""
Importing the useful tools

"""

import gensim.downloader  #Useful to dowload the glove (~ word2vec)
import stanza             #Useful to prerpocess strings (tokenize and lemmatization)
import PyPDF2 #Useful to change PDF to string
import numpy as np 
from gensim.parsing.preprocessing import strip_non_alphanum 
from gensim.parsing.preprocessing import split_alphanum    # Spliting alpha and num : 0.3mm = 0.3 mm"
from gensim.parsing.preprocessing import remove_stopwords  # preprocessign method to remove stop words
from gensim.parsing.preprocessing import strip_numeric      
import os
from nltk.tag import UnigramTagger  #Used to learn tag from a specific word using a corpus
from nltk.corpus import treebank  #the corpus

"""Trainning the tagger : this tagger is useful to know the type of syntaxic token it is without knowing its context"""

train_sentences = treebank.tagged_sents()[:2500]
Uni_tagger = UnigramTagger(train_sentences)

os.environ['KMP_DUPLICATE_LIB_OK']='True'  #Used to avoid some common errors

""" Tokenisation an lemmatisation preprocessing using stanza"""

nlp = stanza.Pipeline(lang='en', processors='tokenize,lemma', use_gpu=True, dir = 'D:/Cours/MRDI/I&AM²/Python/CoreNLP')  #Change dir to the location to save the dowloaded model

"""Dowloading the glove model to have a word embedding model"""

wiki_vectors = gensim.downloader.load('glove-wiki-gigaword-300')

""" Define the prerpocessing methods to use  with gensim"""

CUSTOM_FILTERS = [remove_stopwords, split_alphanum, strip_non_alphanum, strip_numeric]

"""removing manually somme "useless words" and removing some syntaxic type of words"""

ban_word = ['be','have','part',',','.','to','its','will','and']
ban_pos = ['DT', 'WDT','PRP','IN','EX','CD','RB','MD','TO','CC','PRP$']

def preprocess(text):
    """Takes raw text and return a list of list (one list by sentences) of preprocessed sentences"""
    doc = nlp(text)   #using stanza to tokenize and lemmatize and spliting the senteces
    New_sentences = []
    for sent in doc.sentences:
        sentence = []
        for word in sent.words:
            if word.lemma not in ban_word:
                
                if word.upos == None:
                    #If a word as no tag using our trained unitagger to find one
                    wordupos = Uni_tagger.tag([word.lemma])[0][1]
                else:
                    wordupos = word.upos
                    
                if wordupos not in ban_pos:       #if this syntaxic type is not ban save the word reduce version (word.lemma )     
                    sentence.append(word.lemma)  
        New_sentences.append(sentence)
    return New_sentences

def wikisimilars(word,n_similar):
    """ Taking a word and give the expanded version (as a list of word) of this word according to glove trained on wiki
    The size of the expanded representation is defined by n_similar"""
    L = []
    try:
        for close_word in wiki_vectors.most_similar(word, topn= n_similar):   #most similar give the most similar word (topn first) according to glove
            if preprocess(close_word[0]) != [[]]:
                L.append(close_word[0])
    except:
        pass
    return L

"""Define the hyper parameters wordsbytoken wich represent the size of the expanded representation for our sentences"""

wordsbytoken = 5

def expanded_representation(sentence_tokens):
    """Define the expanded representation of a senteces (as a list) by taking the expanded representation of each word"""
    expanded_representation = []
    for token in sentence_tokens:
        expanded_representation = expanded_representation + [token] + wikisimilars(token,wordsbytoken)
    return expanded_representation

def chunk_representation(chunk):
    """Define the expanded representation of a chunk (as a list) by taking the expanded representation of each word"""
    sentencesrepr = [sentence.exp_representation for sentence in chunk]
    chunkrepr = []
    for sent in sentencesrepr:
        for token in sent:
            chunkrepr.append(token)
    return chunkrepr
       
def similarity(wordsA,wordsB):
    """ Takes two chunk of words (two list) and give back the similarity score and the trigger words associated with the score"""
    Words = wordsA + wordsB
    VectA = np.zeros(len(Words))
    VectB = np.zeros(len(Words))
    
    for i, word in enumerate(Words): #we iterate for each word of the union of vocabulary
        if word in wordsA:
            # the word is in the chunk A set is value to 1 
            VectA[i] = 1
        if word in wordsB:
            VectB[i] = 1
    similarity = np.dot(VectA,VectB)/(np.linalg.norm(VectA)*np.linalg.norm(VectB))  #Using the cosine similarity to define the similarity score between wordsA and wordsB
    trigger_words = []
    
    trigger_words = list(set(wordsA)&set(wordsB))  #define the words responsible for the similarity

    return [similarity, trigger_words]


def pdf_to_text(pdf_path):   
    """https://www.askpython.com/python/examples/convert-pdf-to-txt"""
    
    pdf_file = open(pdf_path,'rb')
    pdf = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf.numPages
    Text = ''
    for p in range(num_pages):
        pageobj=pdf.getPage(p)
        Text += str(pageobj.extractText())
    return Text

def blocnotes_to_text(bn_path):
    txt = '' 
    with open(bn_path , "r") as blocnote:
        lignes = blocnote.readlines()
        # for ligne in lignes:
        #     print(ligne)
        l_net = [ s.strip ("\n\r") for s in lignes ]
    
    for line in l_net:
        txt += str(line)
    
    return txt

def sentence_to_chunks(sentences, N_of_sent_by_chunk):
    """Takes a list of senteces and define a list of chunks made of sequence of N_of_sent_by_chunk sneteces"""
    chunks = []
    i=0
    if i + N_of_sent_by_chunk > len(sentences): #if there is too few senteces
        chunks = [sentences]
    else:
        while i + N_of_sent_by_chunk <= len(sentences):
            chunks.append(sentences[i:i+N_of_sent_by_chunk]) #saving the chunks
            i+=1
    return chunks
        
            
    
    
    
    
    
    
    
    
    